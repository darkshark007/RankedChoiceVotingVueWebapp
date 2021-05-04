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
                                let pollModel = data;
                                pollModel.pollRoute = `/poll/${pollModel.id}`;
                                pollModel.editRoute = `/editPoll/${pollModel.id}`;
                                pollModel.editBallots = `/editBallots/${pollModel.id}`;
                                resolve(pollModel);
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
                            let pollModel = data;
                            pollModel.pollRoute = `/poll/${pollModel.id}`;
                            pollModel.editRoute = `/editPoll/${pollModel.id}`;
                            pollModel.editBallots = `/editBallots/${pollModel.id}`;
                            resolve(pollModel);
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
            choices: [],
            ballots: [],
            ballotsPublic: [],
            pollRoute: '',
            editRoute: '',
            editBallots: '',
        };
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