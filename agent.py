import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from livekit.agents import Agent, AgentSession, JobContext, RunContext, WorkerOptions, cli, function_tool
from livekit.plugins import deepgram, groq, cartesia, silero

import db

load_dotenv(".env.local")
db.init_db()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vet-agent")


@function_tool
async def consultar_horarios(context: RunContext, data: str):
    """Consulta horários disponíveis na clínica para uma data (formato YYYY-MM-DD)."""
    disponiveis = db.horarios_disponiveis(data)
    if not disponiveis:
        return {"disponivel": False, "mensagem": "Sem horários livres nesse dia."}
    return {"disponivel": True, "horarios": disponiveis}


@function_tool
async def marcar_consulta(context: RunContext, tutor: str, pet: str, data: str, hora: str):
    """Marca uma consulta veterinária. data em YYYY-MM-DD, hora em HH:MM."""
    ok, msg = db.agendar(tutor, pet, data, hora)
    if not ok:
        alternativas = db.horarios_disponiveis(data)
        return {"sucesso": False, "mensagem": msg, "alternativas": alternativas}
    return {"sucesso": True, "mensagem": msg}


class RecepcionistaVet(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "Você é a recepcionista virtual de uma clínica veterinária. "
                f"Hoje é {datetime.now().strftime('%Y-%m-%d')}. "
                "Colete: nome do tutor, nome do pet, data e horário desejado. "
                "Sempre confira horários disponíveis antes de marcar. "
                "Se o horário já estiver ocupado, ofereça as alternativas retornadas pela ferramenta. "
                "Seja breve e natural, como uma ligação de telefone real."
            ),
            tools=[consultar_horarios, marcar_consulta],
        )


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-3", language="pt"),
        llm=groq.LLM(model="openai/gpt-oss-120b"),
        tts=cartesia.TTS(model="sonic-2", language="pt", voice="79a125e8-cd45-4c13-8a67-188112f4dd22"),
    )

    await session.start(agent=RecepcionistaVet(), room=ctx.room)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))