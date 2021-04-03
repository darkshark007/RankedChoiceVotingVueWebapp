<template>
    <div class="fish">
        Fish
    </div>
</template>

<script>
module.exports = {
    name: 'red-poll-component',
    data: () => {
        return {};
    },
    mounted: () => {
        console.log('Red Poll Component mounted');
    },
};
</script>

<style scoped>
    .fish {
        color: red;
    }
</style>
