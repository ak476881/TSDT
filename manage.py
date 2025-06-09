import sys
import subprocess

def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "runserver":
        # 直接运行 view.py，相当于 flask run
        subprocess.run([sys.executable, "views.py"])
    else:
        print("Usage: python manage.py runserver")

if __name__ == "__main__":
    main()
