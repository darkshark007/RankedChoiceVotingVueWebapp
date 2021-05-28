<template>
    <div id="myPolls" align="center">
        <v-container>
            <v-card
                class="wrapper appWidth"
                id="loading-card"
                v-if="loading"
                :loading="loading"
            ></v-card>
            <message-card
                :errorString=errorString
                errorStringBase="Error loading Polls: "
            ></message-card>
            <v-card
                class="wrapper appWidth"
                v-if="!loading"
            >
                <v-card-title>
                    My Polls
                </v-card-title>
                <v-divider class="mx-4"></v-divider>
                <div v-if="polls.length === 0">
                    You don't have any Polls yet!
                </div>
                <div v-for="poll, idx in polls" :key="idx">
                    <router-link :to="poll.route" class="route-item">
                        <v-row align=center>
                            <v-col cols=1>
                                <v-icon class="ma-3">mdi-chart-box</v-icon>
                            </v-col>
                            <v-col cols=10>
                                <v-card-text>{{ poll.name }}</v-card-text>
                            </v-col>
                        </v-row>
                    </router-link>
                </div>
            </v-card>
            <v-card
                class="wrapper appWidth"
                v-if="!loading"
            >
                <v-card-title>
                    Public Polls
                </v-card-title>
                <v-divider class="mx-4"></v-divider>
                <div v-if="publicPolls.length === 0">
                    There are no Public polls!
                </div>
                <div v-for="poll, idx in publicPolls" :key="idx">
                    <router-link :to="poll.route" class="route-item">
                        <v-row align=center>
                            <v-col cols=1>
                                <v-icon class="ma-3">mdi-chart-box</v-icon>
                            </v-col>
                            <v-col cols=10>
                                <v-card-text>{{ poll.name }}</v-card-text>
                            </v-col>
                        </v-row>
                    </router-link>
                </div>
            </v-card>
        </v-container>
    </div>
</template>

<script>
import MessageCard from '../components/MessageCard.vue';
import Utils from '../utils.js';

export default {
    name: 'my-polls',
    components: {
        'message-card': MessageCard,
    },
    data: () => {
        return {
            errorString: null,
            loading: false,
            polls: [],
            publicPolls: [],
        };
    },
    methods: {
        loadMyPolls() {
            this.loading = true;
            Utils.get(window['API'].get_my_polls)
                .then(response => {
                    if (response.status === 200) {
                        return response.json()
                            .then(data => {
                                this.polls = data.polls.sort((a, b) => (a.updated > b.updated) ? -1 : 1);
                                for (let pollIdx = 0; pollIdx < this.polls.length; pollIdx++) {
                                    let current = this.polls[pollIdx];
                                    current.route = `/poll/${current.id}`;
                                }
                                this.publicPolls = data.public.sort((a, b) => (a.updated > b.updated) ? -1 : 1);
                                for (let pollIdx = 0; pollIdx < this.publicPolls.length; pollIdx++) {
                                    let current = this.publicPolls[pollIdx];
                                    current.route = `/poll/${current.id}`;
                                }
                            });
                    } else {
                        return response.text()
                            .then(text => {
                                this.errorString = text;
                            });
                    }
                })
                .catch((error) => {
                    this.errorString = error;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
    },
    mounted() {
        this.loadMyPolls();
    },
};
</script>

<style scoped>
</style>