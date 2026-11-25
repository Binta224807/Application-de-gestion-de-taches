<template>
    <div class="company-page">
        <div class="page-header anim-fade-up">
            <Building2 :size="30" class="header-icon" />
            <div>
                <h1>Mon organisation</h1>
                <p class="subtitle">
                    Espace collaboratif de votre équipe
                </p>
            </div>
        </div>

        <!-- ============================ -->
        <!-- MEMBRE D'UNE ORGANISATION    -->
        <!-- ============================ -->
        <template v-if="company">
            <div class="info-card anim-fade-up">
                <div class="info-head">
                    <div>
                        <h2>{{ company.name }}</h2>
                        <p v-if="company.description" class="muted">
                            {{ company.description }}
                        </p>
                    </div>
                    <span v-if="myTitle" class="title-badge">
                        {{ myTitle }}
                    </span>
                </div>

                <div v-if="isAdmin" class="invite-row">
                    <div>
                        <label>Code d'invitation</label>
                        <p class="muted">
                            Partagez ce code pour inviter des membres
                        </p>
                    </div>
                    <div class="invite-code">
                        <code>{{ company.invite_code }}</code>
                        <button class="btn-ghost" @click="copyCode">
                            <Copy :size="14" /> Copier
                        </button>
                    </div>
                </div>

                <button
                    v-if="!isOwner"
                    class="btn-danger-ghost"
                    @click="leaveOrg"
                >
                    <LogOut :size="15" /> Quitter l'organisation
                </button>
            </div>

            <!-- MEMBRES -->
            <div class="members-card anim-fade-up">
                <h3>
                    <Users :size="18" /> Membres
                    <span class="count">{{ members.length }}</span>
                </h3>

                <div class="member-list">
                    <div
                        v-for="m in members"
                        :key="m.id"
                        class="member-row"
                    >
                        <div class="member-avatar">
                            {{ m.username.charAt(0).toUpperCase() }}
                        </div>

                        <div class="member-info">
                            <strong>{{ m.username }}</strong>
                            <small v-if="m.is_owner">Propriétaire</small>
                            <small v-else-if="m.is_admin">Administrateur</small>
                        </div>

                        <template v-if="isAdmin && !m.is_owner">
                            <input
                                class="title-input"
                                :value="m.title"
                                placeholder="Titre (ex. Chef de projet)"
                                @change="updateMember(m, { title: $event.target.value })"
                            />
                            <label class="admin-toggle">
                                <input
                                    type="checkbox"
                                    :checked="m.is_admin"
                                    @change="updateMember(m, { is_admin: $event.target.checked })"
                                />
                                Admin
                            </label>
                        </template>

                        <span v-else class="member-title">
                            {{ m.title || "—" }}
                        </span>
                    </div>
                </div>
            </div>
        </template>

        <!-- ============================ -->
        <!-- PAS D'ORGANISATION           -->
        <!-- ============================ -->
        <template v-else>
            <div class="choice-grid stagger">
                <div class="choice-card">
                    <PlusCircle :size="28" class="choice-icon" />
                    <h3>Créer une organisation</h3>
                    <p>
                        Entreprise, association, équipe, startup…
                        définissez vos propres rôles.
                    </p>

                    <form @submit.prevent="createOrg">
                        <input
                            v-model="createForm.name"
                            placeholder="Nom de l'organisation"
                            required
                        />
                        <input
                            v-model="createForm.title"
                            placeholder="Votre titre (ex. Directeur)"
                        />
                        <textarea
                            v-model="createForm.description"
                            placeholder="Description (optionnel)"
                            rows="2"
                        ></textarea>
                        <select v-model="createForm.kind">
                            <option value="organization">Organisation</option>
                            <option value="company">Entreprise</option>
                            <option value="startup">Startup</option>
                            <option value="association">Association</option>
                            <option value="team">Équipe</option>
                            <option value="project">Projet collectif</option>
                        </select>
                        <button class="btn-primary" type="submit">
                            Créer
                        </button>
                    </form>
                </div>

                <div class="choice-card">
                    <UserPlus :size="28" class="choice-icon" />
                    <h3>Rejoindre une organisation</h3>
                    <p>
                        Vous avez reçu un code d'invitation ?
                        Entrez-le ici.
                    </p>

                    <form @submit.prevent="joinOrg">
                        <input
                            v-model="joinCode"
                            placeholder="CODE D'INVITATION"
                            class="code-input"
                            required
                        />
                        <button class="btn-primary" type="submit">
                            Rejoindre
                        </button>
                    </form>
                </div>
            </div>
        </template>

        <p v-if="message" class="message" :class="{ error: isError }">
            {{ message }}
        </p>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import { spaceState, isAdmin, setSpace } from "../services/space";
import {
    Building2, Users, Copy, LogOut, PlusCircle, UserPlus,
} from "lucide-vue-next";

const router = useRouter();

const company = ref(null);
const members = ref([]);
const myTitle = ref("");
const isOwner = ref(false);

const createForm = ref({
    name: "",
    title: "",
    description: "",
    kind: "organization",
});
const joinCode = ref("");
const message = ref("");
const isError = ref(false);

const notify = (text, error = false) => {
    message.value = text;
    isError.value = error;
    setTimeout(() => (message.value = ""), 4000);
};

const loadCompany = async () => {
    const { data } = await api.get("companies/");

    if (!data.length) {
        company.value = null;
        return;
    }

    company.value = data[0];
    isOwner.value = data[0].owner === spaceState.user?.id;

    const { data: m } = await api.get(
        `companies/${company.value.id}/members/`
    );

    members.value = m;
    const me = m.find((x) => x.id === spaceState.user?.id);
    myTitle.value = me?.title || "";
};

const createOrg = async () => {
    try {
        const { data } = await api.post("companies/", {
            name: createForm.value.name,
            description: createForm.value.description,
            kind: createForm.value.kind,
            title: createForm.value.title,
        });
        setSpace(data.id);
    } catch {
        notify("Impossible de créer l'organisation.", true);
    }
};

const joinOrg = async () => {
    try {
        const { data } = await api.post("companies/join/", {
            invite_code: joinCode.value,
        });
        setSpace(data.company.id);
    } catch (e) {
        notify(
            e.response?.data?.error || "Code invalide.",
            true
        );
    }
};

const leaveOrg = async () => {
    try {
        await api.post("companies/leave/");
        setSpace("personal");
    } catch (e) {
        notify(
            e.response?.data?.error || "Erreur.",
            true
        );
    }
};

const updateMember = async (member, patch) => {
    try {
        await api.patch(
            `companies/${company.value.id}/members/`,
            { profile_id: member.profile_id, ...patch }
        );
        notify("Membre mis à jour.");
        await loadCompany();
    } catch {
        notify("Modification refusée.", true);
    }
};

const copyCode = async () => {
    await navigator.clipboard.writeText(
        company.value.invite_code
    );
    notify("Code copié !");
};

onMounted(loadCompany);
</script>

<style scoped>
.company-page {
    padding: 32px;
    min-height: 100vh;
    background: transparent;
    color: var(--text);
}

.page-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 28px;
}

.header-icon {
    color: var(--accent);
}

.page-header h1 {
    color: var(--text-h);
    font-family: var(--display);
    font-size: 26px;
    margin: 0;
}

.subtitle {
    margin: 2px 0 0;
    font-size: 13px;
}

.info-card,
.members-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-l);
    padding: 24px;
    margin-bottom: 20px;
}

.info-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
}

.info-head h2 {
    color: var(--text-h);
    margin: 0 0 4px;
}

.muted {
    color: var(--text);
    font-size: 13px;
    margin: 0;
}

.title-badge {
    background: var(--accent-soft);
    border: 1px solid var(--accent-border);
    color: var(--accent);
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
}

.invite-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid var(--border);
}

.invite-row label {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: var(--text-h);
}

.invite-code {
    display: flex;
    align-items: center;
    gap: 10px;
}

.invite-code code {
    background: var(--surface-2);
    border: 1px dashed var(--accent-border);
    padding: 8px 16px;
    border-radius: 10px;
    font-size: 17px;
    letter-spacing: 3px;
    color: var(--accent);
}

.btn-ghost,
.btn-danger-ghost,
.btn-primary {
    border-radius: 10px;
    padding: 9px 16px;
    font-family: inherit;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid var(--border-strong);
    background: transparent;
    color: var(--text-h);
    display: inline-flex;
    align-items: center;
    gap: 7px;
    transition: 0.2s;
}

.btn-ghost:hover {
    border-color: var(--accent-border);
    color: var(--accent);
}

.btn-danger-ghost {
    margin-top: 20px;
    color: var(--danger);
    border-color: rgba(239, 68, 68, 0.4);
}

.btn-danger-ghost:hover {
    background: rgba(239, 68, 68, 0.12);
}

.btn-primary {
    background: var(--accent-strong);
    border: none;
    color: white;
    justify-content: center;
}

.btn-primary:hover {
    background: var(--accent);
}

.members-card h3 {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-h);
    margin: 0 0 18px;
}

.count {
    background: var(--accent-soft);
    color: var(--accent);
    font-size: 11px;
    padding: 2px 9px;
    border-radius: 999px;
}

.member-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.member-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 12px;
}

.member-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: var(--accent);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    flex-shrink: 0;
}

.member-info {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.member-info strong {
    color: var(--text-h);
    font-size: 14px;
}

.member-info small {
    color: var(--text);
    font-size: 11px;
}

.title-input {
    flex: 1;
    margin-left: auto;
    max-width: 240px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 7px 10px;
    color: var(--text-h);
    font-size: 12px;
}

.admin-toggle {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: var(--text);
    cursor: pointer;
    white-space: nowrap;
}

.member-title {
    margin-left: auto;
    color: var(--text);
    font-size: 12px;
}

.choice-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
    gap: 20px;
}

.choice-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-l);
    padding: 28px;
    transition: border-color 0.2s, transform 0.2s;
}

.choice-card:hover {
    border-color: var(--accent-border);
    transform: translateY(-3px);
}

.choice-icon {
    color: var(--accent);
    margin-bottom: 14px;
}

.choice-card h3 {
    color: var(--text-h);
    margin: 0 0 8px;
}

.choice-card p {
    font-size: 13px;
    margin: 0 0 18px;
}

.choice-card form {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.choice-card input,
.choice-card textarea,
.choice-card select {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 11px 14px;
    color: var(--text-h);
    font-family: inherit;
    font-size: 14px;
}

.choice-card input:focus,
.choice-card textarea:focus,
.choice-card select:focus {
    outline: none;
    border-color: var(--accent-border);
}

.code-input {
    letter-spacing: 3px;
    text-transform: uppercase;
    text-align: center;
    font-weight: 700;
}

.message {
    margin-top: 16px;
    color: var(--success);
    font-size: 14px;
}

.message.error {
    color: var(--danger);
}

@media (max-width: 640px) {
    .company-page {
        padding: 16px;
    }

    .title-input {
        max-width: 100%;
    }

    .member-row {
        flex-wrap: wrap;
    }
}
</style>
