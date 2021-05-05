import Utils from './utils.js';

export default {
    // Poll Helper Functions
    getPollData(data) {
        return new Promise((resolve, reject) => {
            Utils.get(window['API'].get_poll_data, data)
                .then(response => {
                    if (response.status === 200) {
                        return response.json()
                            .then(data => {
                                resolve(this.processPollData(data));
                            });
                    } else {
                        return response.text()
                            .then(text => {
                                reject(text);
                            });
                    }
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    savePoll(pollModel) {
        return new Promise((resolve, reject) => {
            Utils.post(window['API'].create_or_update_poll, pollModel)
            .then(response => {
                if (response.status === 200) {
                    return response.json()
                        .then(data => {
                            resolve(this.processPollData(data));
                        });
                } else {
                    return response.text()
                        .then(text => {
                            reject(text);
                        });
                }
            })
            .catch((error) => {
                reject(error);
            });
        });
    },
    getEmptyPollContext() {
        return {
            id: null,
            name: '',
            type: '',
            description: '',
            publicPoll: false,
            publicBallots: "maybe",
            multiBallotsPerUser: true,
            locked: false,
            randomizeChoices: true,
            choices: [],
            ballots: [],
            ballotsPublic: [],
            pollRoute: '',
            editRoute: '',
            editBallots: '',
        };
    },
    processPollData(data) {
        let pollModel = {
            ...this.getEmptyPollContext(),
            ...data,
        }
        pollModel.pollRoute = `/poll/${pollModel.id}`;
        pollModel.editRoute = `/editPoll/${pollModel.id}`;
        pollModel.editBallots = `/editBallots/${pollModel.id}`;

        if (pollModel.randomizeChoices) {
            this.shuffle(pollModel.choices);
        }

        for (let ballotKey in pollModel.ballots) {
            let ballot = pollModel.ballots[ballotKey];
            ballot.route = `/editBallots/${pollModel.id}/${ballot.id}`;
        }

        return pollModel;
    },


    // Ballot Helper Functions
    getBallotData(pollId, ballotId) {
        return new Promise((resolve, reject) => {
            if (pollId && ballotId) {
                let data = {
                    'pollId': pollId,
                    'ballotId': ballotId,
                };
                Utils.get(window['API'].get_ballot_data, data)
                    .then(response => {
                        if (response.status === 200) {
                            return response.json()
                                .then(data => {
                                    let ballotContext = data;
                                    resolve(ballotContext);
                                });
                        } else {
                            return response.text()
                                .then(text => {
                                    reject(text);
                                });
                        }
                    })
                    .catch((error) => {
                        reject(error);
                    });
            } else {
                reject('No ID passed!');
            }
        });
    },
    saveBallot(ballotData) {
        return new Promise((resolve, reject) => {
            Utils.post(window['API'].create_or_update_ballot, ballotData)
            .then(response => {
                if (response.status === 200) {
                    return response.json()
                        .then((data) => {
                            // let pollModel = data;
                            // pollModel.pollRoute = `/poll/${pollModel.id}`;
                            // pollModel.editRoute = `/editPoll/${pollModel.id}`;
                            // pollModel.editBallots = `/editBallots/${pollModel.id}`;
                            resolve(data);
                        });
                } else {
                    return response.text()
                        .then(text => {
                            reject(text);
                        });
                }
            })
            .catch((error) => {
                reject(error);
            });
        });
    },
    getEmptyBallotContext() {
        return {
            name: '',
            id: null,
            publicBallot: false,
            context: {},
        };
    },


    // Choice Helper Functions
    getEmptyChoiceContext() {
        return {
            name: '',
            description: '',
        };
    },


    // Other Helper Functions
    shuffle(array) {
        // Based on Fischer-Yates Knuth Shuffle
        //   "How to randomize (shuffle) a JavaScript array?"
        //       >>> https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
        var currentIndex = array.length, temporaryValue, randomIndex;

        // While there remain elements to shuffle...
        while (0 !== currentIndex) {
            // Pick a remaining element...
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex -= 1;

            // And swap it with the current element.
            temporaryValue = array[currentIndex];
            array[currentIndex] = array[randomIndex];
            array[randomIndex] = temporaryValue;
        }

        return array;
    },

    // Data Filters/Transformers
    filters: {
        displayDate(date) {
            let dt = new Date(date);
            let hour = ""+dt.getHours();
            if (hour.length === 1) {
                hour = "0"+hour;
            }
            let min = ""+dt.getMinutes();
            if (min.length === 1) {
                min = "0"+min;
            }
            return `${dt.getMonth()}/${dt.getDate()}/${dt.getFullYear()} ${hour}:${min}`;
        },
        displayPollType(type) {
            let item = window['POLL_TYPES'].find((t) => {
                return t[0] === type;
            });
            if (item)
                return item[1];
            return null;
        },
        titleCase(val) {
            return `${val}`
                .split(" ")
                .map((w) => w.substring(0,1).toUpperCase()+w.substring(1))
                .join(" ");
        },
    },

    // Data/Constants
    data: {
        pollTypeList: function() {
            let mapping = window.POLL_TYPES.map((typ) => {
                return {
                    'id': typ[0],
                    'name': typ[1],
                };
            });
            return mapping;
        }(),
        // pollTypes: function() {
        //     let mapping = {};
        //     for (let t in window.POLL_TYPES) {
        //         let type = window.POLL_TYPES[t];
        //         mapping[type[0]] = type[0];
        //     }
        //     return mapping;
        // }(),
    },
};