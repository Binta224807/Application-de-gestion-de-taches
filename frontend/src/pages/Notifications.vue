<template>

<div class="notifications-page">

    <!-- HEADER -->

    <div class="notifications-header">

        <div>
            <h1><Bell :size="26" class="page-icon" /> Notifications</h1>
            <p>Consultez vos notifications et accédez aux tâches associées.</p>
        </div>

        <button
            v-if="unreadCount > 0"
            class="mark-all-btn"
            @click="markAllRead"
        >
            Tout marquer comme lu
        </button>

    </div>


    <!-- LOADING -->

    <div
        v-if="loading"
        class="loading"
    >
        Chargement...
    </div>


    <!-- VIDE -->

    <div
        v-else-if="notifications.length === 0"
        class="empty"
    >
        <span class="notif-icon"><Bell :size="18" /></span>
        <h2>Aucune notification</h2>
        <p>Vous n'avez pas de notification pour le moment.</p>
    </div>


    <!-- LISTE -->

    <div
        v-else
        class="notifications-list"
    >

        <div
            v-for="notification in sortedNotifications"
            :key="notification.id"
            class="notification-card"
            :class="{ unread: !notification.is_read }"
            @click="handleClick(notification)"
        >

            <div class="notification-dot" v-if="!notification.is_read"></div>

            <div class="notification-content">

                <h3>{{ notification.title }}</h3>

                <p>{{ notification.message }}</p>

                <div class="notification-meta">

                    <span>
                        {{ formatDate(notification.created_at) }}
                    </span>

                    <span v-if="notification.task_title">
                        Tâche : {{ notification.task_title }}
                    </span>

                </div>

            </div>

            <button
                v-if="!notification.is_read"
                class="mark-read-btn"
                @click.stop="markRead(notification)"
            >
                Marquer comme lu
            </button>

        </div>

    </div>


</div>

</template>


<script setup>
import { Bell } from "lucide-vue-next";

import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const router = useRouter();

const notifications = ref([]);
const loading = ref(true);


const sortedNotifications = computed(() => {

    return [...notifications.value].sort((a, b) => {

        return new Date(b.created_at) - new Date(a.created_at);

    });

});


const unreadCount = computed(() => {

    return notifications.value.filter(
        n => !n.is_read
    ).length;

});


const loadNotifications = async () => {

    try {

        loading.value = true;

        const response = await api.get("notifications/");

        notifications.value = response.data;

    }

    catch (error) {

        console.error("Erreur notifications :", error);

    }

    finally {

        loading.value = false;

    }

};


const markRead = async (notification) => {

    try {

        await api.post(`notifications/${notification.id}/read/`);

        notification.is_read = true;

    }

    catch (error) {

        console.error("Erreur lecture :", error);

    }

};


const markAllRead = async () => {

    try {

        await api.post("notifications/read-all/");

        notifications.value.forEach(
            n => n.is_read = true
        );

    }

    catch (error) {

        console.error("Erreur tout lire :", error);

    }

};


const handleClick = async (notification) => {

    if (!notification.is_read) {

        await markRead(notification);

    }

    if (notification.task) {

        router.push(`/tasks/${notification.task}`);

    }

};


const formatDate = (dateString) => {

    if (!dateString) return "";

    return new Date(dateString).toLocaleString("fr-FR", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });

};


onMounted(() => {

    loadNotifications();

});


</script>


<style scoped>

.notifications-page {

    padding: 32px;
    min-height: 100vh;
    background: #020617;
    color: white;

}


.notifications-header {

    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
    flex-wrap: wrap;
    gap: 16px;

}


.notifications-header h1 {

    font-size: 32px;
    font-weight: 800;
    margin: 0 0 8px 0;

}


.notifications-header p {

    color: #94a3b8;
    margin: 0;

}


.mark-all-btn {

    background: #2563eb;
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 12px;
    cursor: pointer;
    font-weight: 600;
    transition: .2s;

}


.mark-all-btn:hover {

    background: #1d4ed8;

}


.loading {

    color: #94a3b8;
    text-align: center;
    padding: 60px;

}


.empty {

    min-height: 350px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    color: #94a3b8;
    text-align: center;

}


.empty span {

    font-size: 60px;

}


.empty h2 {

    color: white;
    margin: 16px 0 6px;

}


.notifications-list {

    display: flex;
    flex-direction: column;
    gap: 12px;

}


.notification-card {

    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 20px;
    border-radius: 16px;
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.08);
    cursor: pointer;
    transition: .2s;

}


.notification-card:hover {

    border-color: #2563eb;

}


.notification-card.unread {

    background: #1e293b;
    border-color: rgba(37, 99, 235, 0.3);

}


.notification-dot {

    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #2563eb;
    margin-top: 6px;
    flex-shrink: 0;

}


.notification-content {

    flex: 1;
    min-width: 0;

}


.notification-content h3 {

    margin: 0 0 6px;
    font-size: 16px;
    color: white;

}


.notification-content p {

    margin: 0 0 10px;
    color: #cbd5e1;
    line-height: 1.5;

}


.notification-meta {

    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    font-size: 12px;
    color: #94a3b8;

}


.mark-read-btn {

    background: transparent;
    border: 1px solid #334155;
    color: #cbd5e1;
    padding: 8px 14px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 12px;
    font-weight: 600;
    transition: .2s;
    flex-shrink: 0;

}


.mark-read-btn:hover {

    background: #2563eb;
    color: white;
    border-color: #2563eb;

}


@media (max-width: 768px) {

    .notifications-page {

        padding: 18px;

    }

    .notifications-header h1 {

        font-size: 26px;

    }

    .notification-card {

        flex-direction: column;
        gap: 12px;

    }

    .mark-read-btn {

        width: 100%;

    }

    .notification-content h3 {

        font-size: 15px;

    }

}

</style>
