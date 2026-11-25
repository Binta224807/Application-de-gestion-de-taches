import { reactive, computed } from "vue";
import api from "./api";

const KEY = "active_space";

export const spaceState = reactive({
    user: null,
    spaces: [{ id: "personal", type: "personal", name: "Espace personnel", is_admin: true }],
    current: localStorage.getItem(KEY) || "personal",
    loaded: false,
});

export const isPersonal = computed(
    () => spaceState.current === "personal"
);

export const activeSpace = computed(() =>
    spaceState.spaces.find(
        (s) => String(s.id) === String(spaceState.current)
    ) || spaceState.spaces[0]
);

export const isAdmin = computed(
    () => isPersonal.value || !!activeSpace.value?.is_admin
);

export const spaceName = computed(() =>
    isPersonal.value
        ? "votre espace personnel"
        : activeSpace.value?.name || "votre organisation"
);

export async function loadSpaces() {
    const { data } = await api.get("me/");

    spaceState.user = data;
    spaceState.spaces = data.spaces;

    const saved = localStorage.getItem(KEY);
    const ids = data.spaces.map((s) => String(s.id));

    if (saved && ids.includes(saved)) {
        spaceState.current = saved;
    } else {
        spaceState.current =
            data.company_id != null
                ? String(data.company_id)
                : "personal";
    }

    _syncLegacy();
    spaceState.loaded = true;
}

export function setSpace(id) {
    spaceState.current = String(id);
    localStorage.setItem(KEY, spaceState.current);
    _syncLegacy();
    window.location.reload();
}

function _syncLegacy() {
    const admin = isAdmin.value ? "1" : "0";
    localStorage.setItem("is_admin", admin);
    localStorage.setItem("is_ceo", admin);

    const sp = activeSpace.value;
    if (sp && sp.type === "organization") {
        localStorage.setItem("company_id", String(sp.id));
        localStorage.setItem("company_name", sp.name);
    } else {
        localStorage.removeItem("company_id");
        localStorage.setItem("company_name", "votre espace personnel");
    }
}

export function resetSpace() {
    spaceState.user = null;
    spaceState.spaces = [
        { id: "personal", type: "personal", name: "Espace personnel", is_admin: true },
    ];
    spaceState.current = "personal";
    spaceState.loaded = false;
    localStorage.removeItem(KEY);
    localStorage.removeItem("is_admin");
    localStorage.removeItem("is_ceo");
    localStorage.removeItem("company_id");
    localStorage.removeItem("company_name");
}
