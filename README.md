\# Agente de Voz - Agendamento Veterinário



Agente de voz feito com LiveKit Agents que atende ligações e agenda consultas

para uma clínica veterinária, com verificação de conflito de horários via

constraint UNIQUE no SQLite.



\## Stack

\- LiveKit Agents (Python)

\- Deepgram (STT)

\- Groq (LLM - openai/gpt-oss-120b)

\- Cartesia (TTS)

\- SQLite



\## Como rodar

1\. `python -m venv venv \&\& venv\\Scripts\\activate`

2\. `pip install -r requirements.txt`

3\. Preencher `.env.local` com suas chaves (ver `.env.example`)

4\. `python agent.py console`

