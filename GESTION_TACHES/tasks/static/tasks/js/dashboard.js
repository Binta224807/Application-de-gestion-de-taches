

const ctx = document.getElementById('graphique');

  new Chart(ctx, {
        type:'bar',
        data: {
            labels: ['Personnel', 'Famille', 'Études', 'Professionnels', 'Divertissements'],
            datasets: [{
                label: 'Nombre de tâches',
                data: [
                  personnelCount,
                  familleCount,
                  etudesCount,
                  professionnelsCount,
                  divertissementsCount

                ],

                backgroundColor: [
                    "#72b3cf",
                    "#22c55e",
                    "#f59e0b",
                    "#ef4444",
                    "#a855f7"
                ]
            
            }]

        },
        options: {
            responsive: true,
            plugins:{
                legend: {
                    position:'bottom'
                }
            }
        }

    });

class NotificationEngine {
  constructor() {
    this.history = [];
    this.maxHistory = 10;

    this.messages = {
      etudes: {
        normal: [
          "Tu es bien régulier dans tes études aujourd’hui.",
          "Bonne continuité dans ton travail académique.",
          "Ton rythme d’étude est stable et efficace.",
          "Tu avances correctement sur tes objectifs scolaires."
        ],
        motivation: [
          "Une petite session maintenant peut changer ta journée.",
          "Commence par 20 minutes de révision.",
          "Ton avenir dépend de ce que tu fais aujourd’hui.",
          "Reste concentré, tu es sur la bonne voie."
        ],
        alert: [
          "Tes études sont en baisse aujourd’hui.",
          "Attention, tu dois te recentrer sur tes cours.",
          "La régularité est la clé de ta réussite.",
          "Tu risques de perdre du rythme académique."
        ]
      },

      professionnel: {
        normal: [
          "Tes tâches professionnelles avancent bien.",
          "Bonne organisation de ton travail.",
          "Tu gères correctement tes priorités.",
          "Continue sur cette dynamique."
        ],
        motivation: [
          "Commence une petite tâche pour débloquer ton flow.",
          "Avancer maintenant peut débloquer ton projet.",
          "Chaque action compte dans ton évolution.",
          "Concentre-toi sur une tâche simple d’abord."
        ],
        alert: [
          "Tu as des tâches professionnelles en attente.",
          "Attention à l’accumulation de travail.",
          "Ton projet nécessite ton attention.",
          "Ne repousse pas tes responsabilités."
        ]
      },
      famille: {

    normal: [
        "Tu accordes du temps à ta famille.",
        "Bonne présence auprès de tes proches.",
        "Ton équilibre familial est stable."
    ],

    motivation: [
        "Prends un moment pour appeler un proche.",
        "Essaie de passer plus de temps avec ta famille.",
        "Les relations familiales sont importantes."
    ],

    alert: [
        "Tu négliges un peu ta vie familiale.",
        "Attention à garder un équilibre familial.",
        "Ta famille mérite aussi ton attention."
    ]
},

      personnel: {
        normal: [
          "Ton équilibre personnel est correct.",
          "Tu prends soin de toi correctement.",
          "Bonne gestion de ton temps personnel.",
          "Ton rythme de vie est stable."
        ],
        motivation: [
          "Prends un moment pour toi aujourd’hui.",
          "Une pause peut améliorer ta productivité.",
          "Organise ton espace ou ton esprit.",
          "Respire un peu et recentre-toi."
        ],
        alert: [
          "Ton bien-être personnel est négligé.",
          "Attention à la surcharge mentale.",
          "Tu dois ralentir un peu.",
          "Ton équilibre personnel est fragile."
        ]
      },

      divertissement: {
        normal: [
          "Un peu de détente est bon pour toi.",
          "Profite de ton moment libre.",
          "Repos mental activé.",
          "Bonne gestion de ton temps libre."
        ],
        motivation: [
          "Essaie de réduire légèrement ton temps de distraction.",
          "Reviens à tes priorités après cette pause.",
          "L’équilibre est important.",
          "Le divertissement doit rester contrôlé."
        ],
        alert: [
          "Tu passes trop de temps en distraction.",
          "Attention à la perte de concentration.",
          "Rééquilibre ton emploi du temps.",
          "Le divertissement prend trop de place."
        ]
      }
    };
  }

  // =========================
  // Déterminer le niveau
  // =========================

  getLevel(ratio) {

    if (ratio >= 0.75) return "normal";

    if (ratio >= 0.45) return "motivation";

    return "alert";
  }

  alreadyUsed(message) {
    return this.history.includes(message);
  }

  saveToHistory(message) {

    this.history.push(message);

    if (this.history.length > this.maxHistory) {
      this.history.shift();
    }
  }

  generate(category, ratio) {

    const level = this.getLevel(ratio);

    const pool = this.messages[category][level];

    let message;

    do {
      message = pool[Math.floor(Math.random() * pool.length)];
    }

    while (this.alreadyUsed(message));

    this.saveToHistory(message);

    return message;
  }
}

const engine = new NotificationEngine();

const notifBox = document.getElementById("notif-box");

const total =
  personnelCount +
  familleCount +
  etudesCount +
  professionnelsCount +
  divertissementsCount ;
const ratios = {

    personnel: personnelCount / total,

    famille: familleCount / total,

    etudes: etudesCount / total,

    professionnel: professionnelsCount / total,

    divertissement: divertissementsCount / total
};

const notifications = [];

for (const category in ratios) {

    const ratio = ratios[category];

    const message = engine.generate(category, ratio);

    notifications.push(message);
}

notifications.forEach(msg => {

    notifBox.innerHTML += `

        <div class="notification">

            ${msg}

        </div>

    `;
});