import os
from project import app
print(app.debug)
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
