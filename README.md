# my-telegram-bot
Personal telegram bot lambda

## Architecture

```mermaid
flowchart TB
    subgraph Users["사용자"]
        TG_USER[("Telegram 사용자")]
        OTHER_LAMBDA["다른 Lambda"]
    end

    subgraph Telegram["Telegram"]
        TG_API["Telegram API"]
    end

    subgraph AWS["AWS Cloud"]
        subgraph APIGateway["API Gateway"]
            ENDPOINT["/send-telegram<br/>POST"]
        end

        subgraph Lambda["Lambda Function"]
            HANDLER["handler.hello()"]
        end

        SQS[("SQS Queue<br/>MyQueue")]
    end

    subgraph CI_CD["CI/CD"]
        GH_ACTIONS["GitHub Actions"]
        SERVERLESS["Serverless Framework"]
    end

    %% 메시지 흐름
    TG_USER -->|"1. 메시지 전송"| TG_API
    TG_API -->|"2. Webhook"| ENDPOINT
    ENDPOINT -->|"3. 트리거"| HANDLER
    HANDLER -->|"4. 응답 전송"| TG_API
    TG_API -->|"5. 응답 수신"| TG_USER

    %% SQS 흐름
    OTHER_LAMBDA -->|"메시지 발행"| SQS
    SQS -->|"트리거"| HANDLER

    %% 배포 흐름
    GH_ACTIONS -->|"master push"| SERVERLESS
    SERVERLESS -->|"deploy"| Lambda
```

## 주요 구성요소

| 구성요소 | 설명 |
|---------|------|
| **Telegram API** | 봇 메시지 수신/발신 |
| **API Gateway** | HTTP POST 엔드포인트 제공 |
| **Lambda** | Python 3.6 핸들러 (handler.hello) |
| **SQS** | 비동기 메시지 큐 (다른 Lambda 연동용) |
| **GitHub Actions** | master 브랜치 push 시 자동 배포 |

## 메시지 흐름

1. **직접 메시지**: Telegram → Webhook → API Gateway → Lambda → Telegram 응답
2. **SQS 메시지**: 다른 Lambda → SQS → Lambda → Telegram 전송
