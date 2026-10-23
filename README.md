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

O arquivo `agent.py` carrega as variáveis de ambiente de `.env.local`. Copie o modelo seguro, que contém somente exemplos fictícios:

```powershell
Copy-Item .env.example .env.local
```

Edite `.env.local` e substitua **todos** os valores de exemplo pelas credenciais das suas próprias contas:

| Variável | Finalidade |
| --- | --- |
| `LIVEKIT_URL` | URL do projeto/servidor LiveKit |
| `LIVEKIT_API_KEY` / `LIVEKIT_API_SECRET` | Autenticação no LiveKit |
| `DEEPGRAM_API_KEY` | Reconhecimento de fala |
| `GROQ_API_KEY` | Modelo de linguagem |
| `CARTESIA_API_KEY` | Síntese de voz |

A leitura dessas variáveis é feita pelos SDKs/plugins usados em `agent.py`. Nomes conferidos na documentação oficial de [LiveKit](https://docs.livekit.io/deploy/custom/deployments/) e [Groq no LiveKit](https://docs.livekit.io/agents/models/llm/groq/). `.env.local`, outros arquivos `.env` e bancos locais ficam ignorados pelo Git; apenas `.env.example` deve ser versionado. Nunca publique chaves reais.

Para abrir o modo de console:

```powershell
.\.venv\Scripts\python.exe agent.py console
```

Use apenas dados fictícios na demonstração. O funcionamento completo depende da configuração e disponibilidade dos provedores de voz e linguagem; não é uma aplicação inteiramente offline.

## Escopo

O repositório demonstra a integração entre uma sessão de voz, funções de consulta/agendamento e persistência. O modo de console não comprova, sozinho, implantação em produção ou telefonia pública configurada.

## Testes locais sem credenciais

Com Python 3.10 ou superior, os testes de SQLite usam apenas a biblioteca padrão e um banco temporário:

```powershell
python -m unittest discover -s tests -v
```

A suíte verifica horários livres, persistência, rejeição de reserva duplicada, isolamento por data e texto tratado como dado nas consultas SQL. Não acessa provedores, microfone ou banco real.

`requirements.txt` preserva as versões declaradas pelo projeto. Os testes do banco não validam a resolução de todas essas dependências nem a integração completa de voz. Esta revisão não executou chamadas a LiveKit/Deepgram/Groq/Cartesia; essa demonstração depende das credenciais, disponibilidade dos modelos, permissões de áudio e eventuais custos das suas contas.

O código atual ainda permite datas e horários arbitrários nas chamadas diretas ao banco; validações de domínio são um próximo passo. O projeto é um trabalho de estudo e portfólio, sem implantação em produção comprovada.
