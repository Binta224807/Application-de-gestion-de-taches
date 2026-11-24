<script setup>
import { ref, onMounted } from "vue";

const stars = ref([]);
const shooters = ref([]);
const motes = ref([]);
const beams = ref([]);

const rand = (min, max) => Math.random() * (max - min) + min;

onMounted(() => {
    stars.value = Array.from({ length: 130 }, (_, i) => ({
        id: i,
        left: rand(0, 100) + "%",
        top: rand(0, 100) + "%",
        size: rand(1, 2.2) + "px",
        duration: rand(2.5, 7) + "s",
        delay: rand(0, 7) + "s",
        base: rand(0.15, 0.55),
    }));

    shooters.value = Array.from({ length: 5 }, (_, i) => ({
        id: i,
        top: rand(4, 60) + "%",
        duration: rand(9, 16) + "s",
        delay: rand(0, 12) + "s",
    }));

    motes.value = Array.from({ length: 26 }, (_, i) => ({
        id: i,
        left: rand(2, 98) + "%",
        size: rand(2, 5) + "px",
        duration: rand(11, 22) + "s",
        delay: rand(0, 20) + "s",
        drift: rand(-50, 50) + "px",
    }));

    beams.value = Array.from({ length: 3 }, (_, i) => ({
        id: i,
        top: rand(15, 85) + "%",
        duration: rand(10, 18) + "s",
        delay: rand(0, 14) + "s",
    }));
});
</script>

<template>
    <div class="starfield" aria-hidden="true">
        <span
            v-for="s in stars"
            :key="s.id"
            class="star"
            :style="{
                left: s.left,
                top: s.top,
                width: s.size,
                height: s.size,
                animationDuration: s.duration,
                animationDelay: s.delay,
                opacity: s.base,
            }"
        />
        <span
            v-for="m in motes"
            :key="'m' + m.id"
            class="mote"
            :style="{
                left: m.left,
                width: m.size,
                height: m.size,
                animationDuration: m.duration,
                animationDelay: m.delay,
                '--drift': m.drift,
            }"
        />
        <span
            v-for="b in beams"
            :key="'b' + b.id"
            class="beam"
            :style="{
                top: b.top,
                animationDuration: b.duration,
                animationDelay: b.delay,
            }"
        />
        <span
            v-for="sh in shooters"
            :key="'sh' + sh.id"
            class="shooting-star"
            :style="{
                top: sh.top,
                animationDuration: sh.duration,
                animationDelay: sh.delay,
            }"
        />
    </div>
</template>

<style scoped>
.starfield {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
}

/* --- étoiles scintillantes --- */

.star {
    position: absolute;
    border-radius: 50%;
    background: rgba(226, 232, 240, 0.9);
    animation-name: twinkle;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;
}

@keyframes twinkle {
    0%,
    100% {
        opacity: 0.08;
        transform: scale(0.8);
    }
    50% {
        opacity: 0.9;
        transform: scale(1.25);
    }
}

/* --- particules qui montent --- */

.mote {
    position: absolute;
    bottom: -10px;
    border-radius: 50%;
    background: rgba(147, 197, 253, 0.5);
    filter: blur(0.6px);
    animation-name: rise;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
}

@keyframes rise {
    0% {
        transform: translate(0, 0);
        opacity: 0;
    }
    8% {
        opacity: 0.7;
    }
    90% {
        opacity: 0.25;
    }
    100% {
        transform: translate(var(--drift), -105vh);
        opacity: 0;
    }
}

/* --- traits fins qui balayent l'écran --- */

.beam {
    position: absolute;
    left: -30%;
    width: 60%;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(96, 165, 250, 0.5),
        rgba(226, 232, 240, 0.7),
        rgba(96, 165, 250, 0.5),
        transparent
    );
    opacity: 0;
    animation-name: beam-sweep;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;
}

@keyframes beam-sweep {
    0% {
        transform: translateX(0) scaleX(0.4);
        opacity: 0;
    }
    10% {
        opacity: 0.85;
    }
    55% {
        transform: translateX(180vw) scaleX(1);
        opacity: 0.5;
    }
    70%,
    100% {
        transform: translateX(180vw) scaleX(1);
        opacity: 0;
    }
}

/* --- étoiles filantes --- */

.shooting-star {
    position: absolute;
    right: -12%;
    width: 160px;
    height: 1px;
    background: linear-gradient(
        -90deg,
        rgba(255, 255, 255, 0.85),
        rgba(147, 197, 253, 0.35),
        transparent
    );
    border-radius: 2px;
    opacity: 0;
    animation-name: shoot;
    animation-timing-function: ease-in;
    animation-iteration-count: infinite;
    filter: drop-shadow(0 0 4px rgba(147, 197, 253, 0.6));
}

@keyframes shoot {
    0% {
        transform: rotate(-32deg) translateX(0);
        opacity: 0;
    }
    4% {
        opacity: 1;
    }
    16% {
        transform: rotate(-32deg) translateX(-145vw);
        opacity: 0;
    }
    100% {
        transform: rotate(-32deg) translateX(-145vw);
        opacity: 0;
    }
}
</style>
