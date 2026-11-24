<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";

const canvas = ref(null);

let ctx, raf, w, h;
let stars = [], nodes = [], shooters = [];
const mouse = { x: -9999, y: -9999 };
const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");

function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = canvas.value.clientWidth;
    h = canvas.value.clientHeight;
    canvas.value.width = w * dpr;
    canvas.value.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    seed();
}

function seed() {
    stars = Array.from({ length: 150 }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        r: Math.random() * 1.4 + 0.4,
        p: Math.random() * Math.PI * 2,
        s: Math.random() * 1.6 + 0.5,
    }));
    nodes = Array.from({ length: Math.min(90, Math.floor(w / 18)) }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
    }));
    shooters = [];
}

function drawStars(t) {
    for (const s of stars) {
        const a = 0.12 + 0.6 * (0.5 + 0.5 * Math.sin((t / 1000) * s.s + s.p));
        ctx.globalAlpha = a;
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, 6.283);
        ctx.fillStyle = "#dbe7ff";
        ctx.fill();
    }
    ctx.globalAlpha = 1;
}

function drawNetwork() {
    for (const n of nodes) {
        n.x += n.vx;
        n.y += n.vy;
        if (n.x < -30) n.x = w + 30;
        if (n.x > w + 30) n.x = -30;
        if (n.y < -30) n.y = h + 30;
        if (n.y > h + 30) n.y = -30;
    }

    ctx.lineWidth = 1;
    for (let i = 0; i < nodes.length; i++) {
        const a = nodes[i];
        for (let j = i + 1; j < nodes.length; j++) {
            const b = nodes[j];
            const dx = a.x - b.x, dy = a.y - b.y;
            const d = Math.hypot(dx, dy);
            if (d < 135) {
                ctx.globalAlpha = (1 - d / 135) * 0.32;
                ctx.strokeStyle = "#4a6fa5";
                ctx.beginPath();
                ctx.moveTo(a.x, a.y);
                ctx.lineTo(b.x, b.y);
                ctx.stroke();
            }
        }

        ctx.globalAlpha = 0.85;
        ctx.beginPath();
        ctx.arc(a.x, a.y, 1.5, 0, 6.283);
        ctx.fillStyle = "rgba(150, 190, 255, 0.9)";
        ctx.fill();

        const mdx = a.x - mouse.x, mdy = a.y - mouse.y;
        const md = Math.hypot(mdx, mdy);
        if (md < 170) {
            ctx.globalAlpha = (1 - md / 170) * 0.55;
            ctx.strokeStyle = "#60a5fa";
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(mouse.x, mouse.y);
            ctx.stroke();
        }
    }
    ctx.globalAlpha = 1;
}

function drawShooters() {
    if (Math.random() < 0.005 && shooters.length < 3) {
        shooters.push({
            x: w * 0.25 + Math.random() * w * 0.8,
            y: Math.random() * h * 0.45,
            vx: -(9 + Math.random() * 5),
            vy: 5.5 + Math.random() * 3,
            life: 1,
        });
    }

    ctx.lineWidth = 1.4;
    ctx.lineCap = "round";
    for (const sh of shooters) {
        sh.x += sh.vx;
        sh.y += sh.vy;
        sh.life -= 0.011;
        const len = 15;
        const grad = ctx.createLinearGradient(
            sh.x, sh.y,
            sh.x - sh.vx * len, sh.y - sh.vy * len
        );
        grad.addColorStop(0, `rgba(255,255,255,${Math.max(sh.life, 0)})`);
        grad.addColorStop(1, "rgba(147,197,253,0)");
        ctx.strokeStyle = grad;
        ctx.beginPath();
        ctx.moveTo(sh.x, sh.y);
        ctx.lineTo(sh.x - sh.vx * len, sh.y - sh.vy * len);
        ctx.stroke();
    }
    shooters = shooters.filter(
        (s) => s.life > 0 && s.x > -250 && s.y < h + 250
    );
}

function tick(t) {
    ctx.clearRect(0, 0, w, h);
    drawStars(t);
    drawNetwork();
    drawShooters();
    raf = requestAnimationFrame(tick);
}

function onMouse(e) {
    const rect = canvas.value.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
}

function onLeave() {
    mouse.x = -9999;
    mouse.y = -9999;
}

onMounted(() => {
    ctx = canvas.value.getContext("2d");
    resize();
    window.addEventListener("resize", resize);

    if (reduced.matches) {
        drawStars(0);
        return;
    }

    window.addEventListener("mousemove", onMouse);
    window.addEventListener("mouseleave", onLeave);
    raf = requestAnimationFrame(tick);
});

onBeforeUnmount(() => {
    cancelAnimationFrame(raf);
    window.removeEventListener("resize", resize);
    window.removeEventListener("mousemove", onMouse);
    window.removeEventListener("mouseleave", onLeave);
});
</script>

<template>
    <canvas ref="canvas" class="starfield" aria-hidden="true" />
</template>

<style scoped>
.starfield {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
}
</style>
