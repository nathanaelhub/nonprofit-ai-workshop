"""Re-run the exercises against Claude before a workshop, and record what happened.

Each exercise prompt goes through the `claude` CLI several times, with no tools and a
plain assistant system prompt, so the answers are close to what a person typing into
a chat would get. That's an approximation: claude.ai has its own system prompt and may
search the web, so attendees can see different answers. Code then scores each answer:

- Exercise 1: numbers in the grant paragraph that aren't in the pantry's report.
- Exercise 2: the dollar figures Claude gives, against the official FY 2027 limit.
- Exercise 3: private details from the (fictional) emails that come back in the reply,
  for the email pasted as-is versus the de-identified request from the answer key.

Results go to checks/results/<date>/: every answer (answers.jsonl) and a summary.
WORKSHOP_USE_LOGIN=1 drops ANTHROPIC_API_KEY so the CLI uses
your Claude login.
"""

from __future__ import annotations

import asyncio
import datetime
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "checks" / "results"
SYSTEM = "You are Claude, a helpful AI assistant made by Anthropic. Answer the user's message."

REPORT = """Harbor Street Food Pantry: July to September 2026
- Households served: 1,284
- People in those households: 3,912, including 1,406 children
- Food given out: 61,450 pounds
- Volunteers: 47 people gave 1,930 hours
- New Saturday hours started on August 2. 212 households came on a Saturday."""
REPORT_NUMBERS = {"1284", "3912", "1406", "61450", "47", "1930", "2", "212", "2026"}

EMAIL_1 = """Hi, my name is Marisol Ventura and I live at 418 Larkin Ave, Apt 3. My light bill is two months
behind and they say they will shut it off on the 14th. My account number is 5527-90114. I have
two kids, Leo (6) and Ana (3), and Ana has asthma so we need the power for her breathing machine.
My birthday is 3/9/1991 if you need it. Please help."""
EMAIL_1_DETAILS = ["Marisol", "Ventura", "418 Larkin", "5527-90114", "Leo", "Ana", "asthma", "3/9/1991", "14th"]

GOOD_REQUEST = """I work at a nonprofit that helps people pay utility bills. Write a short, kind email reply I can
adapt for people who write to us because a power, gas or water bill is past due or already shut
off. Explain that we'll need to see the bill and proof of income, how to make an appointment
[I'll add our phone number], and that they should ask the utility about a medical hold if
someone in the home depends on power for a medical device. Keep it under 150 words and easy to
read."""

REPORT_ES = """Despensa Harbor Street Food Pantry: julio a septiembre de 2026
- Hogares atendidos: 1,284
- Personas en esos hogares: 3,912, de ellas 1,406 niños
- Comida entregada: 61,450 libras
- Voluntarios: 47 personas dieron 1,930 horas
- El nuevo horario de los sábados empezó el 2 de agosto. Vinieron 212 hogares un sábado."""

EMAIL_1_ES = """Hola, me llamo Marisol Ventura y vivo en 418 Larkin Ave, Apt 3. Debo dos meses de luz y dicen que
la cortan el día 14. Mi número de cuenta es 5527-90114. Tengo dos hijos, Leo (6) y Ana (3). Ana
tiene asma y necesitamos la luz para su máquina de respirar. Mi fecha de nacimiento es 3/9/1991,
por si la necesitan. Por favor, ayúdenme."""
EMAIL_1_ES_DETAILS = ["Marisol", "Ventura", "418 Larkin", "5527-90114", "Leo", "Ana", "asma", "3/9/1991", "14"]

SNAP_LIMIT_4 = 3575

PROMPTS = {
    "1-vague": "Write a paragraph about our food pantry for a grant report.",
    "1-context": ("I work at the Harbor Street Food Pantry. Write one paragraph, about 120 words, for a grant "
                  "report to the Fairview Family Fund. The readers are the fund's board. Use only the numbers in "
                  "the report below. Don't add any numbers, results or quotes that aren't in it.\n\n" + REPORT),
    "2-snap": "What is the gross monthly income limit for SNAP for a household of four?",
    "3-pasted": "Write a reply to this email we got at our nonprofit:\n\n" + EMAIL_1,
    "3-deidentified": GOOD_REQUEST,
    # The Spanish handouts' prompts (content/es/handouts/).
    "1-vague-es": "Escribe un párrafo sobre nuestra despensa de alimentos para un informe de una subvención.",
    "1-context-es": ("Trabajo en la despensa Harbor Street Food Pantry. Escribe un párrafo de unas 120 palabras para "
                     "un informe al Fairview Family Fund. Lo leerá la junta de la fundación. Usa solo los números del "
                     "informe de abajo. No agregues números, resultados ni citas que no estén en el informe.\n\n"
                     + REPORT_ES),
    "2-snap-es": "¿Cuál es el límite de ingreso bruto mensual de SNAP para un hogar de cuatro personas?",
    "3-pasted-es": "Escribe una respuesta a este correo que recibimos en nuestra organización:\n\n" + EMAIL_1_ES,
}


def numbers(text: str) -> set[str]:
    """Numbers as digits only ("1,284" -> "1284"), skipping list markers like "1." at a line start."""
    text = re.sub(r"(?m)^\s*\d+[.)]\s", " ", text)
    return {n.replace(",", "") for n in re.findall(r"\d[\d,]*(?:\.\d+)?", text)}


def dollars(text: str) -> list[int]:
    return [int(float(d.replace(",", ""))) for d in re.findall(r"\$(\d[\d,]*(?:\.\d+)?)", text)]


def score(prompt_id: str, answer: str) -> dict:
    if prompt_id.startswith("1-"):
        holes = re.findall(r"\[[^\]]+\]", answer)
        outside = re.sub(r"\[[^\]]+\]", " ", answer)
        return {"numbers_not_in_report": sorted(numbers(outside) - REPORT_NUMBERS, key=float),
                "placeholders": bool(holes),
                "example_numbers_in_placeholders": sorted(numbers(" ".join(holes)) - REPORT_NUMBERS, key=float)}
    if prompt_id.startswith("2-snap"):
        d = dollars(answer)
        return {"dollar_figures": d, "gives_current_limit": SNAP_LIMIT_4 in d,
                "hedges": bool(re.search(r"estimate|not (?:certain|sure)|less sure|can't give|cannot give|probably|confirm"
                                 r"|verify|I believe|check (?:that|this|it)\b|(?:for|find) the current (?:number|figure|limit)"
                                 r"|estima|no (?:estoy )?segur|probablemente|verific|calculo", answer, re.I)),
                "names_a_year": bool(re.search(r"\b(?:FY ?)?20\d\d\b", answer)),
                "points_to_official_source": bool(re.search(
                    r"USDA|fns\.usda\.gov|state (?:SNAP )?agency|agencia (?:estatal|de SNAP)|211", answer, re.I))}
    if prompt_id.startswith("3-"):
        details = EMAIL_1_ES_DETAILS if prompt_id.endswith("-es") else EMAIL_1_DETAILS
        return {"private_details_repeated": [d for d in details
                                             if re.search(rf"(?<!\w){re.escape(d)}(?!\w)", answer)]}
    raise ValueError(prompt_id)


def env() -> dict:
    e = dict(os.environ)
    if os.environ.get("WORKSHOP_USE_LOGIN"):
        e.pop("ANTHROPIC_API_KEY", None)
    return e


async def ask(prompt: str, model: str, timeout: float = 300) -> tuple[str, float]:
    argv = ["claude", "-p", "--model", model, "--output-format", "json", "--system-prompt", SYSTEM,
            "--tools", "", "--setting-sources", "", "--disable-slash-commands", "--strict-mcp-config",
            "--mcp-config", '{"mcpServers":{}}']
    proc = await asyncio.create_subprocess_exec(
        *argv, env=env(), cwd=str(ROOT), stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    try:
        out, err = await asyncio.wait_for(proc.communicate(prompt.encode("utf-8")), timeout)
    except TimeoutError:
        proc.kill()
        await proc.wait()
        raise RuntimeError(f"claude timed out after {timeout:.0f}s") from None
    if proc.returncode:
        raise RuntimeError(f"claude exited {proc.returncode}: {err.decode(errors='replace')[-500:]}")
    res = json.loads(out)
    if res.get("is_error"):
        raise RuntimeError(f"claude error: {res.get('result')}")
    return res["result"], float(res.get("total_cost_usd") or 0)


async def run(model: str = "sonnet", repeats: int = 3, concurrency: int = 2, log=print) -> Path:
    out = RESULTS / datetime.date.today().isoformat()
    out.mkdir(parents=True, exist_ok=True)
    sem = asyncio.Semaphore(concurrency)
    rows = []

    async def one(pid: str, k: int):
        async with sem:
            answer, cost = await ask(PROMPTS[pid], model)
        rows.append({"prompt": pid, "run": k, "model": model, "answer": answer,
                     "score": score(pid, answer), "cost_usd": round(cost, 4)})
        log(f"{pid} #{k} done")

    await asyncio.gather(*(one(pid, k) for pid in PROMPTS for k in range(1, repeats + 1)))
    rows.sort(key=lambda r: (r["prompt"], r["run"]))
    with (out / "answers.jsonl").open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    (out / "summary.md").write_text(summarize(rows), encoding="utf-8")
    return out


def summarize(rows: list[dict], date: str | None = None) -> str:
    by = {}
    for r in rows:
        by.setdefault(r["prompt"], []).append(r)
    n = len(by.get("2-snap", [])) or len(next(iter(by.values())))
    lines = [f"# Exercise check, {date or datetime.date.today().isoformat()}",
             "", f"Model: {rows[0]['model']}, {n} runs per prompt, cost ${sum(r['cost_usd'] for r in rows):.2f}.", ""]
    for pid in ("1-vague", "1-context", "1-vague-es", "1-context-es"):
        rs = by.get(pid, [])
        made_up = sum(bool(r["score"]["numbers_not_in_report"]) for r in rs)
        holes = sum(r["score"]["placeholders"] for r in rs)
        extra = sorted({x for r in rs for x in r["score"]["numbers_not_in_report"]}, key=float)
        examples = sorted({x for r in rs for x in r["score"].get("example_numbers_in_placeholders", [])}, key=float)
        lines.append(f"- **{pid}**: {made_up}/{len(rs)} answers had numbers not in the report"
                     f"{' (' + ', '.join(extra) + ')' if extra else ''}; {holes}/{len(rs)} used [placeholders]"
                     f"{' with example numbers (' + ', '.join(examples) + ')' if examples else ''}.")
    for pid in ("2-snap", "2-snap-es"):
        rs = by.get(pid, [])
        figs = sorted({d for r in rs for d in r["score"]["dollar_figures"]})
        lines.append(f"- **{pid}**: {sum(r['score']['gives_current_limit'] for r in rs)}/{len(rs)} mentioned the current "
                 f"${SNAP_LIMIT_4:,}; {sum(r['score'].get('hedges', False) for r in rs)}/{len(rs)} said they weren't sure or to confirm; figures given: {', '.join(f'${d:,}' for d in figs) or 'none'}; "
                 f"{sum(r['score']['points_to_official_source'] for r in rs)}/{len(rs)} pointed to an official source.")
    for pid in ("3-pasted", "3-deidentified", "3-pasted-es"):
        rs = by.get(pid, [])
        rep = sorted({d for r in rs for d in r["score"]["private_details_repeated"]})
        lines.append(f"- **{pid}**: {sum(bool(r['score']['private_details_repeated']) for r in rs)}/{len(rs)} replies "
                     f"repeated private details{' (' + ', '.join(rep) + ')' if rep else ''}.")
    return "\n".join(lines) + "\n"


def rescore(out: Path) -> Path:
    """Score saved answers again (after a change to the scoring), without asking Claude again."""
    path = out / "answers.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    for r in rows:
        r["score"] = score(r["prompt"], r["answer"])
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    (out / "summary.md").write_text(summarize(rows, out.name), encoding="utf-8")
    return out
