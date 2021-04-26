import Utils from './utils.js';

export default {
    // Poll Helper Functions
    getPollData(id) {
        return new Promise((resolve, reject) => {
            if (id) {
                let data = {
                    'id': id,
                };
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
            } else {
                reject('No ID passed!');
            }
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
            choices: [],
            pollRoute: '',
            editRoute: '',
            editBallots: '',
        };
    },


    // Ballot Helper Functions
    emptyBallotContext() {
        return {
            id: null,
            name: '',
            type: '',
            choices: {},
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
            return `${dt.getMonth()}/${dt.getDate()}/${dt.getYear()} ${hour}:${min}`;
        },
        displayPollType(type) {
            let item = window['POLL_TYPES'].find((t) => {
                return t[0] === type;
            });
            if (item)
                return item[1];
            return null;
        },
    },

    // Constants
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
    },
};