import { writable } from "svelte/store";

export const currentTrack = writable("{}");
export const queue = writable([]);
export const queuePosition = writable(0);