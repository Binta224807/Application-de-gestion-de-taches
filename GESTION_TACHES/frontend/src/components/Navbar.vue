<template>

<header class="navbar">

    <!-- MENU MOBILE -->
    <button
        class="mobile-menu"
        @click="emit('toggleMenu')"
        aria-label="Ouvrir le menu"
    >
        ☰
    </button>


    <!-- LOGO / MARQUE -->
    <div class="brand">

        <div class="brand-icon">
            ✓
        </div>

        <div class="brand-text">
            <strong>NOVA</strong>
            <span>TASKS</span>
        </div>

    </div>


    <!-- RECHERCHE -->
    <div class="search-container">

        <div class="search-box">

            <span class="search-icon">
                🔍
            </span>

            <input
                v-model="search"
                @input="updateSearch(search)"
                type="text"
                placeholder="Rechercher une tâche..."
            />

            <span
                v-if="search"
                class="clear-search"
                @click="clearSearch"
            >
                ×
            </span>

        </div>

    </div>


    <!-- PARTIE DROITE -->
    <div class="right-section">

        <!-- PROFIL -->
        <div
            v-if="isAuthenticated"
            class="profile"
        >

            <div class="avatar">
                {{ usernameInitial }}
            </div>

            <div class="user-info">

                <p class="username">
                    {{ username }}
                </p>

                <p class="status">

                    <span class="status-dot"></span>

                    En ligne

                </p>

            </div>

        </div>


        <!-- DECONNEXION -->
        <button
            v-if="isAuthenticated"
            class="logout-btn"
            @click="logout"
        >
            <span>↪</span>
            <span class="logout-text">
                Déconnexion
            </span>
        </button>


        <!-- CONNEXION -->
        <RouterLink
            v-else
            to="/login"
            class="login-btn"
        >
            Connexion
        </RouterLink>

    </div>

</header>

</template>


<script setup>

import {
    ref,
    computed,
    onMounted,
    onBeforeUnmount
} from "vue";

import { useRouter } from "vue-router";

import { useSearch } from "../components/useSearch";


const router = useRouter();

const { updateSearch } = useSearch();

const emit = defineEmits([
    "toggleMenu"
]);


const search = ref("");

const username = ref("Utilisateur");

const isAuthenticated = ref(false);


// =====================================================
// RECUPERATION UTILISATEUR
// =====================================================

const updateUser = () => {

    const access =
        localStorage.getItem("access");

    const accessToken =
        localStorage.getItem("access_token");

    isAuthenticated.value =
        !!(access || accessToken);


    username.value =
        localStorage.getItem("username")
        || "Utilisateur";

};


// =====================================================
// INITIAL
// =====================================================

onMounted(() => {

    updateUser();

    window.addEventListener(
        "storage",
        updateUser
    );

});


// =====================================================
// NETTOYAGE
// =====================================================

onBeforeUnmount(() => {

    window.removeEventListener(
        "storage",
        updateUser
    );

});


// =====================================================
// INITIAL UTILISATEUR
// =====================================================

const usernameInitial = computed(() => {

    return username.value
        .charAt(0)
        .toUpperCase();

});


// =====================================================
// RECHERCHE
// =====================================================

const clearSearch = () => {

    search.value = "";

    updateSearch("");

};


// =====================================================
// DECONNEXION
// =====================================================

const logout = () => {

    localStorage.removeItem("access");
    localStorage.removeItem("refresh");

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    localStorage.removeItem("username");

    isAuthenticated.value = false;

    username.value = "Utilisateur";

    router.push("/login");

};

</script>


<style scoped>

/* =====================================================
   NAVBAR
===================================================== */

.navbar {

    width: 100%;

    min-height: 76px;

    box-sizing: border-box;

    display: flex;

    align-items: center;

    gap: 24px;

    padding: 12px 28px;

    background:
        linear-gradient(
            135deg,
            #020617 0%,
            #0f172a 55%,
            #111827 100%
        );

    border-bottom:
        1px solid rgba(148,163,184,.15);

    box-shadow:
        0 8px 30px rgba(0,0,0,.20);

    position: relative;

    z-index: 100;

}


/* =====================================================
   BRAND
===================================================== */

.brand {

    display: flex;

    align-items: center;

    gap: 10px;

    flex-shrink: 0;

}


.brand-icon {

    width: 40px;

    height: 40px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 12px;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );

    color: white;

    font-size: 20px;

    font-weight: 900;

    box-shadow:
        0 8px 20px rgba(37,99,235,.25);

}


.brand-text {

    display: flex;

    flex-direction: column;

    line-height: 1;

}


.brand-text strong {

    color: white;

    font-size: 15px;

    letter-spacing: 1px;

}


.brand-text span {

    color: #60a5fa;

    font-size: 10px;

    letter-spacing: 2px;

    margin-top: 4px;

}


/* =====================================================
   SEARCH
===================================================== */

.search-container {

    flex: 1;

    display: flex;

    justify-content: center;

    min-width: 0;

}


.search-box {

    width: min(100%, 600px);

    height: 46px;

    display: flex;

    align-items: center;

    gap: 10px;

    box-sizing: border-box;

    padding: 0 15px;

    background:
        rgba(15,23,42,.85);

    border:
        1px solid rgba(148,163,184,.18);

    border-radius: 14px;

    transition: .25s;

}


.search-box:focus-within {

    border-color: #6366f1;

    box-shadow:
        0 0 0 3px rgba(99,102,241,.10);

}


.search-icon {

    font-size: 16px;

    flex-shrink: 0;

}


.search-box input {

    flex: 1;

    min-width: 0;

    border: none;

    outline: none;

    background: transparent;

    color: white;

    font-size: 14px;

}


.search-box input::placeholder {

    color: #64748b;

}


.clear-search {

    color: #94a3b8;

    font-size: 20px;

    cursor: pointer;

    line-height: 1;

}


/* =====================================================
   RIGHT
===================================================== */

.right-section {

    display: flex;

    align-items: center;

    gap: 18px;

    flex-shrink: 0;

}


/* =====================================================
   PROFILE
===================================================== */

.profile {

    display: flex;

    align-items: center;

    gap: 10px;

}


.avatar {

    width: 43px;

    height: 43px;

    min-width: 43px;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );

    color: white;

    font-size: 16px;

    font-weight: 800;

    border:
        2px solid rgba(255,255,255,.10);

}


.user-info {

    display: flex;

    flex-direction: column;

    justify-content: center;

    min-width: 80px;

}


.username {

    color: white;

    font-size: 14px;

    font-weight: 700;

    margin: 0;

    white-space: nowrap;

    max-width: 130px;

    overflow: hidden;

    text-overflow: ellipsis;

}


.status {

    display: flex;

    align-items: center;

    gap: 6px;

    margin: 4px 0 0;

    color: #22c55e;

    font-size: 11px;

}


.status-dot {

    width: 7px;

    height: 7px;

    border-radius: 50%;

    background: #22c55e;

    box-shadow:
        0 0 8px rgba(34,197,94,.7);

}


/* =====================================================
   BUTTONS
===================================================== */

.logout-btn,
.login-btn {

    height: 42px;

    padding: 0 16px;

    display: inline-flex;

    align-items: center;

    justify-content: center;

    gap: 7px;

    border: none;

    border-radius: 12px;

    font-size: 13px;

    font-weight: 700;

    cursor: pointer;

    text-decoration: none;

    white-space: nowrap;

}


.logout-btn {

    color: white;

    background:
        linear-gradient(
            135deg,
            #ef4444,
            #dc2626
        );

}


.login-btn {

    color: white;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );

}


/* =====================================================
   MENU MOBILE
===================================================== */

.mobile-menu {

    display: none;

    width: 42px;

    height: 42px;

    align-items: center;

    justify-content: center;

    border: none;

    border-radius: 12px;

    background: #1e293b;

    color: white;

    font-size: 23px;

    cursor: pointer;

    flex-shrink: 0;

}


/* =====================================================
   TABLETTE
===================================================== */

@media (max-width: 1000px) {

    .navbar {

        gap: 14px;

        padding:
            10px 18px;

    }

    .user-info {

        display: none;

    }

    .logout-text {

        display: none;

    }

    .logout-btn {

        width: 42px;

        padding: 0;

    }

}


/* =====================================================
   MOBILE
===================================================== */

@media (max-width: 768px) {

    .navbar {

        min-height: 64px;

        padding:
            10px 12px;

        gap: 10px;

    }


    .mobile-menu {

        display: flex;

    }


    .brand {

        gap: 0;

    }


    .brand-icon {

        width: 38px;

        height: 38px;

    }


    .brand-text {

        display: none;

    }


    .search-container {

        order: 3;

        flex-basis: 100%;

        width: 100%;

    }


    .navbar {

        flex-wrap: wrap;

    }


    .search-box {

        height: 42px;

        border-radius: 12px;

    }


    .right-section {

        margin-left: auto;

        gap: 8px;

    }


    .avatar {

        width: 38px;

        height: 38px;

        min-width: 38px;

    }


    .profile .user-info {

        display: none;

    }


    .logout-btn {

        width: 38px;

        height: 38px;

        border-radius: 11px;

        font-size: 16px;

    }

}


/* =====================================================
   PETIT TELEPHONE
===================================================== */

@media (max-width: 430px) {

    .navbar {

        padding:
            9px 10px;

    }


    .mobile-menu {

        width: 38px;

        height: 38px;

        font-size: 21px;

    }


    .brand-icon {

        width: 36px;

        height: 36px;

    }


    .right-section {

        gap: 6px;

    }


    .search-container {

        flex-basis: 100%;

    }

}

</style>