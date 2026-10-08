from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nexora 0.2</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f5f7ff;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                text-align: center;
            }

            .box {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                max-width: 500px;
            }

            h1 {
                font-size: 42px;
                margin-bottom: 10px;
            }

            p {
                font-size: 18px;
                color: #555;
            }

            .status {
                margin-top: 25px;
                padding: 12px;
                background: #e8f5e9;
                border-radius: 10px;
                color: #2e7d32;
                font-weight: bold;
            }
        </style>
    </head>

    <body>
        <div class="box">
            <h1>🚀 Nexora 0.2</h1>
            <p>Discover your next opportunity.</p>

            <div class="status">
                Nexora is alive and running!
            </div>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run()