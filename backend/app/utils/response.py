from flask import jsonify

class JsonResponse:
    @staticmethod
    def success(data=None, message="Success"):
        return jsonify({
            "status": "success",
            "message": message,
            "data": data or {}
        }), 200

    @staticmethod
    def error(message="Something went wrong", status_code=400):
        return jsonify({
            "status": "error",
            "message": message
        }), status_code
