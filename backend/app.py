from flask import Flask
import weather
import valorant

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello"

@app.route('/data/weather', methods=['GET'])
def weather():
    return weather.main()

@app.route('/data/valorant/leaderboard/<region>/<isUpdate>', methods=['GET'])
def leaderboard(region, isUpdate):

    if isUpdate == 'true':
        # update with mmr_history_updater.update_all(False, printer=False)
        pass

    return valorant.leaderboard(region)



if __name__ == "__main__":
    app.run(debug=True)