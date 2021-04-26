<template>
    <div id="myPolls" align="center">
        <v-container>
            <v-card
                class="wrapper"
                id="loading-card"
                max-width="60%"
                v-if="loading"
                :loading="loading"
            ></v-card>
            <message-card
                :errorString=errorString
                errorStringBase="Error loading Polls: "
            ></message-card>
            <v-card
                class="wrapper"
                max-width="60%"
                v-if="!loading"
            >
                <v-card-title>
                    My Polls
                </v-card-title>
                <v-divider class="mx-4"></v-divider>
                <div v-for="poll, idx in polls" :key="idx">
                    <router-link :to="poll.route" class="poll-item">
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
            loading: null,
            polls: null,
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
.poll-item {
    text-align: left;
    text-decoration: none;
}
</style>