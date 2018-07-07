from flask import Flask, render_template, request, redirect

app = Flask(__name__)

current_search = ""
links_ = []


@app.route('/')
def homepage():
    global current_search
    current_search = ""
    return render_template('index.html')


@app.route('/results/<int:page_number>')
@app.route('/results/<int:page_number>', methods=["POST"])
def results(page_number):
    from query import find_some, get_query, text_procces
    global current_search, links_
    db_string = "postgres://patrick:Getting started@localhost:5432/database"

    if ('searchquery' in request.form):
        current_search = request.form['searchquery']
        sentence = request.form['searchquery']
        processed_sentence = text_procces(sentence)
        urls = get_query(processed_sentence)
        urls_dict = find_some(urls, list(processed_sentence.keys()))
        urls_list = []
        links_ = []
        for i in urls_dict:
            urls_list.append([i, urls_dict[i]])
        urls_list = sorted(urls_list, key=lambda k: k[1], reverse=True)
        for i in urls_list:
            links_.append(i[0])
    if current_search == "":
        return redirect('/')
    else:
        return render_template('results.html', query=current_search, links=links_, page=page_number,
                               res_cnt=len(links_))


if __name__ == '__main__':
    app.run()