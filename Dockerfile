FROM python:3.9

EXPOSE 8080
EXPOSE 7634

CMD ["python", "script.py", "-d", "downloads"]
