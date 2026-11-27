// Dijalankan dengan js-tiktoken 1.0.21 (npm), 26 Nov 2026: node cek_token.mjs
import { getEncoding } from "js-tiktoken";
const texts = ["strawberry", " strawberry", "Strawberry", "Ada berapa huruf r di strawberry?",
 "How many r's are in strawberry?",
 "s t r a w b e r r y", "s-t-r-a-w-b-e-r-r-y", "S T R A W B E R R Y",
 "Tolong jelaskan cara kerja mesin cuci", "Please explain how a washing machine works",
 "Saya ingin memesan makanan", "I want to order food",
 "Selamat pagi, apa kabar?", "Good morning, how are you?",
 "mempertanggungjawabkan","ketidakadilan","responsibility","rambutan","stroberi"];
for (const name of ["o200k_base","cl100k_base"]) {
  const enc = getEncoding(name);
  console.log("==", name);
  for (const t of texts) { const ids = enc.encode(t); console.log(ids.length, JSON.stringify(ids.map(i=>enc.decode([i]))), JSON.stringify(ids)); }
}
