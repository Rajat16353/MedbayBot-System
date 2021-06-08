import sys
import os
from App.main import app

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'install':
            print("Installing the required dependencies. This may take some time")
            os.system('pip install -r requirements.txt')
            exit()
        elif sys.argv[1] == 'test':
            print("Testing chatbot predictions")
            os.system('python test_predictions.py')
            exit()
    except Exception as e:
        # print(e)
        pass
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)
