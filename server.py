import random
from flask import Flask, render_template

app = Flask(__name__)

with open('nouns.txt') as f:
    nouns = f.readlines()

with open('adjectives.txt') as f:
    adjectives = f.readlines()


def generate_staple():
    return "{} {} {} {}".format(random.choice(adjectives),
                                random.choice(nouns),
                                random.choice(nouns),
                                random.choice(nouns),
                                )



@app.route("/")
def main():
    return render_template('index.html', staple=generate_staple())


if __name__ == "__main__":
    app.run(debug=True)
