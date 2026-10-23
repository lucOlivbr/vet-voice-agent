# Agente de voz para agendamento veterinário

Projeto de estudo em Python que integra reconhecimento de fala, um modelo de linguagem e síntese de voz para consultar horários e agendar atendimentos de uma clínica veterinária de demonstração.

## Tecnologias

- LiveKit Agents com Python para a sessão de voz.
- Deepgram para reconhecimento de fala (STT).
- Groq para o modelo de linguagem (LLM).
- Cartesia para síntese de voz (TTS).
- SQLite para armazenamento dos agendamentos.

O projeto utiliza uma restrição `UNIQUE` no SQLite para impedir conflitos no registro dos horários.

## Executar localmente

Crie um ambiente virtual e instale as dependências. No Windows/PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

O arquivo `agent.py` carrega as variáveis de ambiente de `.env.local`. Crie esse arquivo localmente e configure as credenciais exigidas pelo LiveKit e pelos plugins de Deepgram, Groq e Cartesia. Este repositório não inclui um `.env.example`; consulte a configuração dos provedores utilizados antes de executar. As chaves devem pertencer às suas próprias contas e não devem ser publicadas no GitHub.

Para abrir o modo de console:

```powershell
.\.venv\Scripts\python.exe agent.py console
```

Use apenas dados fictícios na demonstração. O funcionamento completo depende da configuração e disponibilidade dos provedores de voz e linguagem; não é uma aplicação inteiramente offline.

## Escopo

O repositório demonstra a integração entre uma sessão de voz, funções de consulta/agendamento e persistência. O modo de console não comprova, sozinho, implantação em produção ou telefonia pública configurada.

Não foram adicionados testes nem realizada uma nova execução com os provedores nesta revisão de documentação. O projeto é um trabalho de estudo e portfólio.
