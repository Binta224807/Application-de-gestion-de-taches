/**
 * Convertit une durée en minutes en un affichage lisible.
 * Exemples :
 *   30  -> "30 min"
 *   60  -> "1 h"
 *   90  -> "1 h 30"
 *   120 -> "2 h"
 */

export const formatDuration = (minutes) => {

  if (minutes === null || minutes === undefined || isNaN(minutes)) {

    return "0 min";

  }

  const total = Number(minutes);

  if (total < 60) {

    return `${total} min`;

  }

  const hours = Math.floor(total / 60);

  const remaining = total % 60;

  if (remaining === 0) {

    return `${hours} h`;

  }

  return `${hours} h ${remaining}`;

};


export const formatDurationShort = (minutes) => {

  return formatDuration(minutes);

};
