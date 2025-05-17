from flask import Blueprint

upload = Blueprint("upload", __name__)  # ✅ Définit un Blueprint Flask

@upload.route("/test-upload", methods=["GET"])
def test_upload():
    return {"message": "Upload route is working!"}
