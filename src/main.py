from flask import Flask
 
from core.config import config
from ui.routes import routes_bp
#admin
from ui.routes import routes_bp
from ui.admin_routes import admin_bp


# Flask uygulaması oluşturulur.
app = Flask(
    __name__,
    static_folder="../assets",
    static_url_path="/assets",
    template_folder="ui/templates"
)
#kampus_etkinlik_final_key
app.secret_key="kampus_etkinlik_final_key"

# Arayüz katmanındaki route yapısı uygulamaya eklenir.
app.register_blueprint(routes_bp)
#admin
app.register_blueprint(admin_bp)


if __name__ == "__main__":
    # Uygulama, config dosyasındaki ayarlar ile başlatılır.
    app.run(
        host=config.host,
        port=config.port,
        debug=config.debug
    )