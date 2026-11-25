<template>

  <aside
    class="sidebar"
    :class="{open: props.open}"
    @click="emit('close')"
  >
    <!-- LOGO -->

    <div class="brand">

      <h1>NOVA TASKS</h1>

      <p>Pilotage d'entreprise</p>

      <span class="brand-signature">by Clever</span>

    </div>


    <!-- SÉLECTEUR D'ESPACE -->

    <div
      v-if="spaceState.spaces.length > 0"
      class="space-switcher"
    >

      <button
        class="space-current"
        @click.stop="spaceMenu = !spaceMenu"
      >

        <component
          :is="isPersonal ? User : Building2"
          :size="15"
        />

        <span class="space-name">
          {{ isPersonal ? "Personnel" : activeSpace?.name }}
        </span>

        <ChevronDown
          :size="14"
          class="chevron"
          :class="{ flipped: spaceMenu }"
        />

      </button>


      <div
        v-if="spaceMenu"
        class="space-menu"
      >

        <button
          v-for="sp in spaceState.spaces"
          :key="sp.id"
          class="space-option"
          :class="{ active: String(sp.id) === spaceState.current }"
          @click.stop="switchSpace(sp.id)"
        >

          <component
            :is="sp.type === 'personal' ? User : Building2"
            :size="14"
          />

          <span>{{ sp.type === "personal" ? "Personnel" : sp.name }}</span>

          <small v-if="sp.title">{{ sp.title }}</small>

        </button>

      </div>

    </div>



    <!-- NAVIGATION -->

    <nav class="menu" @click.stop>

      <RouterLink
        v-for="item in menuItems"
        :key="item.to"
        :to="item.to"
        class="menu-item anim-slide-right"
        :style="{ animationDelay: item.delay }"
       @click="emit('close')">
        <span class="item-index">{{ item.index }}</span>
        <component :is="item.icon" :size="18" :stroke-width="1.8" class="icon" />
        <span class="item-label">{{ item.label }}</span>
      </RouterLink>

    </nav>



    <!-- PROFIL -->

    <div class="profile">


      <div class="avatar">

        {{ initial }}

      </div>



      <div class="user-info">

        <p class="username">
          {{ username }}
        </p>


        <p class="status">

          <span></span>
          {{ roleLabel }}

        </p>


      </div>


    </div>


  </aside>


</template>



<script setup>
import { computed } from "vue";
import {
  LayoutDashboard,
  ClipboardList,
  CalendarDays,
  BarChart3,
  Trash2,
  Building2,
  Bell,
  User,
  ChevronDown,
} from "lucide-vue-next";

const props = defineProps({

  open: {
    type: Boolean,
    default: false
  }

});

const username =
  localStorage.getItem("username")
  || "Utilisateur";

import { ref } from "vue";
import { spaceState, isPersonal, activeSpace, isAdmin, setSpace } from "../services/space";

const spaceMenu = ref(false);

const switchSpace = (id) => {

  spaceMenu.value = false;

  if (String(id) !== spaceState.current) {

    setSpace(id);

  }

};

const roleLabel = computed(() => {

  if (isPersonal.value) return "Personnel";

  return spaceState.user?.title
    || (isAdmin.value ? "Administrateur" : "Membre");

});

const initial = computed(() => {

  return username
    .charAt(0)
    .toUpperCase();

});

const baseItems = [
  { to: "/dashboard",     label: "Tableau de bord", icon: LayoutDashboard },
  { to: "/tasks",         label: "Gestion tâches",  icon: ClipboardList },
  { to: "/calendar",      label: "Calendrier",      icon: CalendarDays },
  { to: "/statistics",    label: "Statistiques",    icon: BarChart3 },
  { to: "/archives",      label: "Corbeille",       icon: Trash2 },
];

const menuItems = computed(() => {

  const items = [...baseItems];

  if (!isPersonal.value) {

    items.push({
      to: "/company",
      label: "Mon organisation",
      icon: Building2,
    });

  }

  items.push({
    to: "/notifications",
    label: "Notifications",
    icon: Bell,
  });

  return items.map((item, i) => ({
    ...item,
    index: String(i + 1).padStart(2, "0"),
    delay: `${0.05 + i * 0.05}s`,
  }));

});

const emit = defineEmits([
  "close"
]);
</script>



<style scoped>


.sidebar {

  width: 280px;

  height: 100vh;

  position: sticky;

  top: 0;

  flex-shrink: 0;

  background: var(--surface);

  border-right: 1px solid var(--border);

  display: flex;

  flex-direction: column;

  padding: 28px 20px;

}


/* BRAND */


.brand {
  padding: 0 8px;
  flex-shrink: 0;
}


.brand h1 {

  font-family: var(--display);

  font-size: 24px;

  font-weight: 700;

  letter-spacing: 2px;

  background: linear-gradient(
    90deg,
    var(--text-h),
    var(--accent),
    var(--text-h)
  );

  background-size: 220% 100%;

  -webkit-background-clip: text;

  background-clip: text;

  -webkit-text-fill-color: transparent;

  animation: gradient-x 6s ease infinite;

}


.brand p {

  margin-top: 6px;

  color: var(--text);

  font-size: 13px;

}


.brand-signature {

  display: block;

  margin-top: 6px;

  color: var(--accent);

  font-size: 13px;

  font-weight: 700;

  letter-spacing: 1px;

}


/* MENU */


.menu {

  margin-top: 40px;

  display: flex;

  flex-direction: column;

  gap: 6px;

  flex: 1;

  min-height: 0;

  overflow-y: auto;

  padding-right: 4px;

}


.menu-item {

  display: flex;

  align-items: center;

  gap: 14px;

  padding: 13px 14px;

  border-radius: var(--radius);

  color: var(--text);

  text-decoration: none;

  font-weight: 500;

  font-size: 14px;

  border: 1px solid transparent;

  transition: background .2s, color .2s, border-color .2s, transform .2s;

}


.item-index {

  font-family: var(--display);

  font-size: 11px;

  font-weight: 600;

  color: var(--text);

  opacity: .5;

  width: 20px;

  flex-shrink: 0;

}


.menu-item .icon {

  flex-shrink: 0;

}


.menu-item:hover {

  background: var(--surface-2);

  color: var(--text-h);

  border-color: var(--border);

  transform: translateX(4px);

}


.menu-item:hover .item-index {

  color: var(--accent);

  opacity: 1;

}


.menu-item:hover .icon {

  animation: icon-wiggle .45s ease;

}


/* PAGE ACTIVE */


.router-link-active {

  background: var(--accent-soft);

  border-color: var(--accent-border);

  color: var(--text-h);

  animation: glow-pulse 3s ease-in-out infinite;

}


.router-link-active .item-index {

  color: var(--accent);

  opacity: 1;

}


.router-link-active .icon {

  color: var(--accent);

}


/* PROFIL */


.profile {

  display: flex;

  align-items: center;

  gap: 14px;

  padding: 20px 8px 0;

  border-top: 1px solid var(--border);

  flex-shrink: 0;

}


.avatar {

  width: 44px;

  height: 44px;

  border-radius: 50%;

  display: flex;

  align-items: center;

  justify-content: center;

  background: var(--accent-strong);

  color: white;

  font-family: var(--display);

  font-weight: 700;

  font-size: 17px;

}


.username {

  color: var(--text-h);

  font-weight: 600;

}


.status {

  display: flex;

  align-items: center;

  gap: 6px;

  color: var(--success);

  font-size: 12px;

}


.status span {

  width: 7px;

  height: 7px;

  border-radius: 50%;

  background: var(--success);

}


@media (max-width:900px){


  .sidebar{

    position: fixed;

    left: 0;

    top: 0;

    height: 100dvh;

    z-index: 1000;

    transform: translateX(-105%);

    transition: transform .38s cubic-bezier(.22,1,.36,1);

    padding-top: max(24px, env(safe-area-inset-top));

    padding-bottom: max(24px, env(safe-area-inset-bottom));

    box-shadow: 24px 0 60px rgba(0,0,0,.45);

  }


  .sidebar.open{

    transform: translateX(0);

  }


}




/* --- Sélecteur d'espace --- */

.space-switcher {

  position: relative;

  padding: 0 18px;

  margin-bottom: 10px;

}


.space-current {

  width: 100%;

  display: flex;

  align-items: center;

  gap: 8px;

  padding: 9px 12px;

  background: var(--surface-2);

  border: 1px solid var(--border);

  border-radius: 10px;

  color: var(--text-h);

  font-family: inherit;

  font-size: 13px;

  font-weight: 600;

  cursor: pointer;

  transition: border-color .2s;

}


.space-current:hover {

  border-color: var(--accent-border);

}


.space-name {

  flex: 1;

  text-align: left;

  overflow: hidden;

  text-overflow: ellipsis;

  white-space: nowrap;

}


.chevron {

  transition: transform .25s;

  color: var(--text);

}


.chevron.flipped {

  transform: rotate(180deg);

}


.space-menu {

  position: absolute;

  left: 18px;

  right: 18px;

  top: calc(100% + 6px);

  z-index: 50;

  background: var(--surface-2);

  border: 1px solid var(--border-strong);

  border-radius: 12px;

  padding: 6px;

  box-shadow: 0 16px 40px rgba(0,0,0,.45);

  animation: scale-in .25s cubic-bezier(.34,1.4,.64,1) both;

}


.space-option {

  width: 100%;

  display: flex;

  align-items: center;

  gap: 8px;

  padding: 9px 10px;

  border: none;

  border-radius: 8px;

  background: transparent;

  color: var(--text);

  font-family: inherit;

  font-size: 13px;

  cursor: pointer;

  transition: background .15s, color .15s;

}


.space-option span {

  flex: 1;

  text-align: left;

  overflow: hidden;

  text-overflow: ellipsis;

  white-space: nowrap;

}


.space-option small {

  color: var(--text);

  opacity: .7;

  font-size: 10px;

}


.space-option:hover {

  background: var(--accent-soft);

  color: var(--text-h);

}


.space-option.active {

  color: var(--accent);

}


</style>
