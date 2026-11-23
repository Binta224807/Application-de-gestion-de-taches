import { ref } from "vue";

const searchQuery = ref("");

export function useSearch() {

    const updateSearch = (value) => {
        searchQuery.value = value;
    };


    return {
        searchQuery,
        updateSearch
    };

}