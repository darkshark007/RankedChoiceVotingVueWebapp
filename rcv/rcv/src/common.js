import Utils from './utils.js';

export default {
    getBound(block, context) {
        console.log(block);
        console.log(context);
    },

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
            // Validate Poll Data
            if (this.methods.validateLimitRankChoices(pollModel.limitRankChoices) !== true) {
                reject('Invalid setting for Limit Rank Choice!');
            }
            if (this.methods.validateLimitChoicesAdded(pollModel.limitChoicesAdded) !== true) {
                reject('Invalid setting for Limit Choices Added!');
            }

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
    recyclePoll(pollModel) {
        return new Promise((resolve, reject) => {
            let data = {
                'id': pollModel.id,
            }
            Utils.post(window['API'].recycle_poll, data)
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
            publicResults: "always",
            multiBallotsPerUser: true,
            allowUsersToSeeArchivedPolls: true,
            allowUsersToEditBallots: true,
            limitRankChoices: null,
            limitChoicesAdded: null,
            usersCanAddChoices: "never",
            ballotStart: null,
            ballotEnd: null,
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
    getBallotData(pollId, ballotId, includeStats) {
        return new Promise((resolve, reject) => {
            if (pollId && ballotId) {
                let data = {
                    'pollId': pollId,
                    'ballotId': ballotId,
                };
                if (includeStats) data['includeStats'] = true;
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
            creator: '',
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
            return `${(dt.getMonth()+1)}/${dt.getDate()}/${dt.getFullYear()} ${hour}:${min}`;
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
        common__now: -1,
        confirmationDialog: false,
        confirmationDialogContext: {},
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

    computed: {
        pollIsOpen() {
            if (!this.__nowInterval) {
                let updateFunc = function() {
                    this.common__now = ~~(new Date()/1000);
                }.bind(this);
                this.__nowInterval = setInterval(updateFunc, 1000);
            }
            if (this.pollModel.ballotStart) {
                if (this.common__now < this.pollModel.ballotStart) {
                    return false
                }
            }
            if (this.pollModel.ballotEnd) {
                if (this.common__now > this.pollModel.ballotEnd) {
                    return false;
                }
            }
            return true;
        },
        pollStatusMessage() {
            if (!this.__nowInterval) {
                let updateFunc = function() {
                    this.common__now = ~~(new Date()/1000);
                }.bind(this);
                this.__nowInterval = setInterval(updateFunc, 1000);
            }
            function getTimeStamp(diff) {
                let seconds = diff % 60;
                diff = (diff - seconds) / 60;
                if (diff === 0) return `${seconds}sec`;
                if (seconds < 10) seconds = `0${seconds}`;
                let minutes = diff % 60;
                diff = (diff - minutes) / 60;
                if (diff === 0) return `${minutes}:${seconds}`;
                if (minutes < 10) minutes = `0${minutes}`;
                let hours = diff % 24;
                diff = (diff - hours) / 24;
                if (diff === 0) return `${hours} hours`;
                let days = diff % 365;
                diff = (diff - days) / 365;
                if (diff === 0) return `${days} days`;
                return "Calculating...";
            }
            if (this.pollModel.recycled) {
                return "Poll is Recycled!";
            }
            if (this.pollModel.locked) {
                return "Poll is Locked!";
            }
            if (this.pollModel.ballotStart) {
                if (this.common__now < this.pollModel.ballotStart) {
                    return `Poll will open in ${getTimeStamp(this.pollModel.ballotStart-this.common__now)}!`;
                }
            }
            if (this.pollModel.ballotEnd) {
                if (this.common__now > this.pollModel.ballotEnd) {
                    return "Poll is Closed!";
                } else {
                    return `Poll will close in ${getTimeStamp(this.pollModel.ballotEnd-this.common__now)}!`;
                }
            }
            return "Poll is Open";
        },
        choiceIdToNameMap() {
            let idToNameMap = {};
            for (let choiceKey in this.pollModel.choices) {
                let choice = this.pollModel.choices[choiceKey];
                idToNameMap[choice['id']] = choice['name'];
            }
            return idToNameMap;
        },
        canEditBallot() {
            return this.pollModel.allowUsersToEditBallots;
        },
        shouldShowChoiceAddButton() {
            if (this.pollModel.canEdit) return true;
            if (this.pollModel.locked) return false;
            if (this.pollModel.usersCanAddChoices === 'never') return false;
            if (this.pollModel.usersCanAddChoices === 'open') {
                this.common__now = ~~(new Date()/1000);
                if (this.common__now < this.pollModel.ballotStart) {
                    return true;
                }
                return false;
            }
            if (this.pollModel.usersCanAddChoices === 'always') return true;
            return true;
        },
        shouldActivateChoiceAddButton() {
            if (this.pollModel.canEdit) return true;
            if (this.pollModel.locked) return false;
            if (this.pollModel.limitChoicesAdded) {
                let count = 0;
                count += this.pollModel.choices.filter((c) => c.created).length;
                if (this.newChoices) count += this.newChoices.length;
                if (count >= this.pollModel.limitChoicesAdded) return false;
            }
            return true;
        },
        shouldShowResultButton() {
            // Poll Creator or Manager can always see results
            if (this.pollModel.canEdit) return true;
            let resultRule = this.pollModel.publicResults;

            // Results are always Available to the voter
            if (resultRule === 'always') {
                return true;
            }

            // Results are unavailable to the voter until after they have submitted a Ballot
            if (resultRule === 'voting') {
                if (this.pollModel.ballots && this.pollModel.ballots.length >= 1) return true;
                if (this.ballotContext && this.ballotContext.id) return true;
                return false;
            }

            // Results are unavailable until after Poll Closes
            if (resultRule === 'closed') {
                this.common__now = ~~(new Date()/1000);
                if (this.pollModel.ballotStart && this.common__now < this.pollModel.ballotStart) return false;
                if (this.pollModel.locked || !this.pollIsOpen) return true;
                return false;
            }

            // Results are never available Publically, only to Poll creator
            return false;
        },
    },

    methods: {
        ballotSimilarity(stats, type) {
            let statToWeightMap = {
                'included': 1,
                'picks': 2,
                'score_picks': 2,
                'preferences': 4,
                'top_n_picks': 4,
            };
            let data = stats[type];
            if (!data) return Number.NaN;
            let categorySum = 0;
            let categoryMax = 0;
            for (let categoryKey in data) {
                let currentCategory = data[categoryKey];
                let statSum = 0;
                for (let statKey in currentCategory) {
                    if (statKey === 'total') continue;
                    let currentStat = currentCategory[statKey];
                    statSum += currentStat;
                }
                let statCount = Object.keys(currentCategory).length-1;
                let categorySimilarity = ((statSum-statCount) / (currentCategory['total']-statCount));
                if (isNaN(categorySimilarity)) categorySimilarity = 0;
                let weight = statToWeightMap[categoryKey]
                categorySum += weight*categorySimilarity;
                categoryMax += weight;
            }
            let ballotSimilarity = Math.floor(10000.0*(categorySum / categoryMax))/100;
            return ballotSimilarity;
        },
        nextStats() {
            for (let idx = 0; idx < this.displayStats.length; idx++) {
                this.displayStats[idx].seen = true;
            }
            this.displayStats = [];
            for (let idx = 0; idx < 5 && idx < this.statsList.length; idx++) {
                let nextStat = this.statsList.splice(0,1)[0];
                this.displayStats.push(nextStat);
                this.statsList.push(nextStat);
            }
        },
        validateLimitRankChoices(value) {
            if (value === null) return true;

            let nF = Number.parseFloat(value);
            let nI = Number.parseInt(value);
            if (isNaN(nI)) return "Must be a number!";
            if ((nF - nI) != 0) return "Must be an Integer!";
            if (nI < 2) return "Must be empty, or a positive integer greater than 1!";
            return true;
        },
        validateLimitChoicesAdded(value) {
            if (value === null) return true;

            let nF = Number.parseFloat(value);
            let nI = Number.parseInt(value);
            if (isNaN(nI)) return "Must be a number!";
            if ((nF - nI) != 0) return "Must be an Integer!";
            if (nI < 1) return "Must be empty, or a positive integer greater than 0!";
            return true;
        },
        openConfirmationDialog(context) {
            this.confirmationDialog = true;
            this.confirmationDialogContext = {
                // Default context
                'title': 'Confirm',
                'text': '',
                'button1Text': 'Cancel',
                'button1Color': 'red',
                'button1Handler': () => {},
                'button2Text': 'OK',
                'button2Color': 'green',
                'button2Handler': () => {},

                // Custom Context
                ...context,
            }
        },
    },
};