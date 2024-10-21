
# Assignment - Task processing system

A high-throughput task proceesing system using asynchronous APIs to send and consume tasks from a message queue.

```bash
.
├── README.md
├── docker
│   ├── Dockerfile
│   └── entrypoint.sh
├── docker-compose.yml
├── env
│   ├── default.env
│   └── test.env
├── requirements.txt
└── src
    ├── controller
    │   ├── __init__.py
    │   └── task_controller.py              #任務處理邏輯
    ├── main.py                             #API router
    ├── model
    │   ├── __init__.py
    │   ├── rabbitmq.py                     # task queue處理 和 rabbitmq連線
    │   └── db.py                           # DB讀寫
    ├── tests
    │   ├── __init__.py
    │   └── test_unit.py
    └── utils
        ├── __init__.py
        ├── config.py                       #讀取環境變數
        ├── connect.py                      #處理資料庫連線
        ├── data_structure.py               
        └── status.py
```
## Setup

執行服務

```bash
  cd assignment

  cp env/default.env .env
  
  docker-compose up --build -d

  docker-compose ps  #確立服務都正常運行
```
停止服務

```bash
  docker-compose down
```

## API Documentation
API 文件 : https://documenter.getpostman.com/view/37208911/2sAXxY3oU1  







    
## Test

服務起來後，根據API文件，執行curl指令或打postman測試  
swagger: http://127.0.0.1:8000/docs

