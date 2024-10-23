<template>
<ul>
    <li v-for="(value, key) in criteria" :key="key">
        {{ key }}: {{ value }}
    </li>
</ul>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
    setup() {
        const criteria = ref({});
        const fetchUserCriteria = async () => {
            try {
                const response = await axios.get(
                    'book-api/get-user-criteria/', {});
                criteria.value = response.data;
            } catch (error) {
                console.error('Error fetching user criteria:', error);
            }
        };

        onMounted(() => {
            fetchUserCriteria();
        });

        return {
            criteria,
        };
    }
}
</script>