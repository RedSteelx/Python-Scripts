from flask import Flask, request

app = Flask(__name__)
files = list()
del_files = list()
latest = list()
@app.route("/api/add",methods=["POST"])
def api_add():
        
        add = request.args.get('add')
        files.append(add)
        latest.insert(0,'Added: ' + add)
        return '' 
        
@app.route("/api/delete",methods=["POST"])
def api_delete():
        
        delete = request.args.get('delete')
        del_files.append(delete)
        latest.insert(0,'Deleted: ' + delete)
        return ''

@app.route("/")
def root():
        
    return '<h1>Latest Decision: {}</h1>\n<h1>Newly added base files: {}</h1>\n<h1>Deleted files: {}</h1>'.format(latest,files,del_files)

if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0",port=8080)
