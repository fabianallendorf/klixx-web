<template>
  <div id="home" class="container">
    <h1 class="title">Verflixxte Klixx Statistixx</h1>
    <div id="graphs">
      <section class="header">
        <Title v-bind:db="database" type="GENERAL" v-if="loaded" />
      </section>
      <div class="row">
        <ColorCorrectionButton
          v-on:toggle="toggleColorBlindness"
          :colorBlindMode="colorBlindMode"
        />
      </div>
      <div class="row">
        <h2 id="allgemein">
          <a href="#allgemein">Allgemein</a>
        </h2>
        <Loader :loading="!loaded" :blankSize="150">
          <Table v-bind:db="database" type="OVERVIEW" />
        </Loader>
      </div>
      <div class="row">
        <h2 id="kronen">
          <a href="#kronen">Wer hat die meisten Kronen?</a>
        </h2>
        <Loader :loading="!loaded">
          <DoughnutChart
            type="CROWNS"
            :db="database"
            :backgroundColor="[larsColor, florentinColor]"
          />
        </Loader>
      </div>
      <div class="row">
        <p>
          Jeder Spieler bekommt eine Krone wenn er während einer Folge die
          meisten Punkte gewonnen hat. Lars ist bockstark, mit einem
          komfortablen Vorsprung an Kronen.
        </p>
        <p>
          Und wenn ihr jetzt denkt <i>Moment mal, da fehlt doch eine Folge</i>,
          liegt ihr goldrichtig.
          <a
            href="https://www.youtube.com/watch?v=YFDjvlRxij0&t=44m48s"
            target="_blank"
            >Am Ende von Folge 102</a
          >
          wurde ein Video nachträglich entfernt, weshalb ich diese Runde nicht
          in die Statistik aufgenommen habe. Dadurch kam es leider zu einem
          Unentschieden. Lars hatte allerdings diese Runde und damit auch diese
          Folge gewonnen.
        </p>
      </div>
      <div class="row">
        <h2 id="runden-gewonnen">
          <a href="#runden-gewonnen">Wer hat die meisten Runden gewonnen?</a>
        </h2>
        <Loader :loading="!loaded">
          <DoughnutChart
            type="WINNERS"
            :db="database"
            :backgroundColor="[larsColor, florentinColor, resultColor]"
          />
        </Loader>
      </div>
      <div class="row">
        <p>
          Lars hat die Nase vorne. Da beißt die Maus kein Faden ab. 7-mal
          unentschieden. Stabile Leistung Lars.
        </p>
      </div>
      <div class="row">
        <h2 id="meisten-punkte">
          <a href="#meisten-punkte">Wer hat die meisten Punkte gewonnen?</a>
        </h2>
        <Loader :loading="!loaded">
          <DoughnutChart
            type="TOTAL_POINTS"
            :db="database"
            :backgroundColor="[larsColor, florentinColor]"
          />
        </Loader>
      </div>
      <div class="row">
        <p>
          Obwohl Lars erwartbar mehr Punkte geholt, da er mehr Runden gewonnen
          hat, ist die Punktedifferenz nicht so eindeutig. Florentin hat also
          effizienter Punkte geholt, womöglich durch cleveren Einsatz der
          Fischkarte oder bei Runden mit hohen Multiplikatoren besser performt.
        </p>
      </div>
      <div class="row">
        <p></p>
      </div>
      <div class="row">
        <h2 id="lars-treffer">
          <a href="#lars-treffer">Lars Treffer</a>
        </h2>
        <Loader :loading="!loaded">
          <Table v-bind:db="database" type="LARS_HIT" />
        </Loader>
      </div>
      <div class="row">
        <h2 id="florentin-treffer">
          <a href="#florentin-treffer">Florentin Treffer</a>
        </h2>
        <Loader :loading="!loaded" :blankSize="750">
          <Table v-bind:db="database" type="FLORENTIN_HIT" />
        </Loader>
      </div>
      <div class="row">
        <p>
          Florentin hat eine deutlich höhere Trefferquote als Lars. Könnte es
          womöglich damit zusammenhängen, dass Florentin kreativer tippt als
          Lars? Lasst uns dazu einen Blick auf die Tippverteilung werfen.
        </p>
      </div>
      <div class="row">
        <h2 id="lars-tippverteilung">
          <a href="#lars-tippverteilung">Lars Tippverteilung</a>
        </h2>
        <h5>Die 30 häufigsten Tipps</h5>
        <Loader :loading="!loaded" :blankSize="750">
          <HorizontalBarChart
            type="LARS_BET"
            :db="database"
            :height="750"
            :backgroundColor="[larsColor]"
          />
        </Loader>
      </div>
      <div class="row">
        <p>
          Hättet ihr mich vor dieser Auswertung gefragt welche Zahl Lars am
          häufigsten getippt hat, hätte ich Haus und Hof auf die
          <strong>333</strong> gesetzt. <em>Bei Issos Keilerei!</em> In Wahrheit
          ist sie nur auf Platz 8. Die <strong>100</strong> ist auf Platz 1.
          Knapp dahinter auf Platz 2 liegt die 11.
        </p>
      </div>
      <div class="row">
        <h2 id="florentin-tippverteilung">
          <a href="#florentin-tippverteilung">Florentin Tippverteilung</a>
        </h2>
        <h5>Die 30 häufigsten Tipps</h5>
        <Loader :loading="!loaded" :blankSize="750">
          <HorizontalBarChart
            type="FLORENTIN_BET"
            :db="database"
            :height="750"
            :backgroundColor="[florentinColor]"
          />
        </Loader>
      </div>
      <div class="row">
        <p>
          Die <strong>5</strong>! nicht die <strong>8</strong>, ist Florentins
          Lieblingstipp. Wer hätte das gedacht? Die 11 ist auch hier vertreten.
          Florentin ist etwas kreativer als Lars. Es ist intressant dass sich
          Florentin auf Ziffern spezialisiert, wobei Lars lieber den
          Schnapszahlen vertraut. Florentins Top 6 sind durch die Bank
          <strong>Ziffern</strong>.
        </p>
      </div>
      <div class="row">
        <h2 id="verteilung-views">
          <a href="#verteilung-views">Verteilung der Viewzahlen</a>
        </h2>
        <h5>Die 30 häufigsten Viewzahlen</h5>
        <Loader :loading="!loaded">
          <HorizontalBarChart
            type="RESULT_FREQUENCY"
            :db="database"
            :height="750"
            :backgroundColor="[resultColor]"
          />
        </Loader>
      </div>
      <div class="row">
        <p>
          Die verflixxte <strong>7</strong> ist die häufigste Viewzahl. Generell
          kommen sehr niedrige Views häufiger vor. Wenn wir uns an Florentins
          Lieblingstipps erinnern, wird deutlicher warum er eine höhere
          Trefferquote hat. Er hat mit der 8, 9, 3 und zweimal mit der 4
          getroffen. Auf jeden Fall keine schlechte Tatik. Ich denke die
          niedrigen Viewzahlen lassen sich dadurch erklären, dass zufällige
          Videos ausgewählt werden. Die Anzahl an Videos mit wenig Views ist
          wesentlich höher.
        </p>
      </div>
      <div class="row">
        <h2 id="abweichung-views">
          <a href="#abweichung-views">Abweichung von den Views</a>
        </h2>
        <Loader :loading="!loaded" :blankSize="1000">
          <BarChart
            type="BET_RESULT_DIFFERENCE"
            :db="database"
            :backgroundColor="[larsColor, florentinColor]"
          />
        </Loader>
      </div>
      <div class="row">
        <p>
          Am häufigsten liegen Lars und Florentin um 21-50 Views daneben. Ob
          dieser Wert signifikant ist, kann ich nicht sagen.
        </p>
      </div>
      <div class="row">
        <h2 id="geier-koenig">
          <a href="#geier-koenig">Wer ist der (echte) Geierkönig? &#129413;</a>
        </h2>
        <Loader :loading="!loaded">
          <VultureKing
            :db="database"
            :larsColor="larsColor"
            :florentinColor="florentinColor"
          />
        </Loader>
      </div>
      <div class="row">
        <h2 id="unter-ueberschaetzen">
          <a href="#unter-ueberschaetzen">Unterschätzen oder überschätzen?</a>
        </h2>
        <Loader :loading="!loaded">
          <BarChart
            type="OVER_OR_UNDER_ESTIMATION"
            :db="database"
            :backgroundColor="[larsColor, florentinColor]"
          />
        </Loader>
      </div>
      <div class="row">
        <p>
          Die Antwort ist eindeutig. Beide haben mehr Runden für sich
          entschieden wenn ihr Tipp kleiner war als die Viewzahl. Inwiefern
          konservativ schätzen eine gute Tatik ist lässt sich schwer sagen.
        </p>
      </div>
      <div class="row">
        <h2 id="drunter-verliert">
          <a href="#drunter-verliert">Wer drunter geht verliert?</a>
        </h2>
        <Loader :loading="!loaded">
          <BarChart
            type="LOWER_SECOND_BETS"
            :db="database"
            :backgroundColor="[larsColor, florentinColor]"
          />
        </Loader>
      </div>
      <div class="row">
        <p>
          Der Unterschied ist nicht wirklich signifikant. Für diese Behauptung
          gibt es also keine hieb- und stichfesten Beweise. Lediglich bei
          Florentin ist der Anteil an verlorenen Runden etwas höher.
        </p>
      </div>
      <div class="row">
        <h2 id="fischkarten-fluch">
          <a href="#fischkarten-fluch">Der Fischkarten-Fluch &#128128;</a>
        </h2>
        <Loader :loading="!loaded">
          <BarChart
            type="FISH_CARD_CURSE"
            :db="database"
            :backgroundColor="[larsColor, florentinColor]"
          />
        </Loader>
      </div>
      <div class="row">
        <p>
          Gibt es ihn? Gibt es ihn nicht? Bisher konnte man nur vermuten. Lass
          uns etwas Licht ins dunkle bringen.
        </p>
        <p>
          Bei Florentin ist der Unterschied kaum bemerkenswert. Leider überwiegt
          der Fluch ein klein wenig. Aber die Hoffnung in die Fischkarte würde
          ich an seiner Stelle nicht aufgeben.
        </p>
        <p>
          Für Lars hat sich der Fischkarten-Fluch in einen Segen verwandelt.
          Satte 14 Runde mehr gewonnen als verloren, bei dem Einsatz der
          Fischkarte. Kein Grund zur Sorge.
        </p>
        <p>
          <strong
            >Persönliches Fazit: Der Fischkarten-Fluch ist nicht real, er kann
            dir nichts tun. &#128031;</strong
          >
        </p>
      </div>
      <hr />
      <div class="row">
        <h5>
          Viele Dinge die hier gezeigt werden, wurden auch 2019 im
          <a
            href="https://forum.rocketbeans.tv/t/statistiken-zu-verflixxte-klixx/59858"
            target="_blank"
            >RBTV Forum</a
          >
          diskutiert. Schade dass ich erst so spät darauf gestoßen bin. Der
          Thread lohnt sich!
        </h5>
      </div>
      <div class="row">
        <h5>
          Ihr habt einen Fehler entdeckt oder einen Verbesserungsvorschlag?
          Lasst es mich wissen indem ihr ein
          <a
            href="https://github.com/fabianallendorf/klixx-data/issues"
            target="_blank"
            >Issue</a
          >
          erstellt. Danke!
        </h5>
      </div>
    </div>
  </div>
</template>

<script>
import BarChart from "./BarChart.vue";
import HorizontalBarChart from "./HorizontalBarChart.vue";
import DoughnutChart from "./DoughnutChart.vue";
import ColorCorrectionButton from "./ColorCorrectionButton.vue";
import VultureKing from "./VultureKing.vue";
import Table from "./Table.vue";
import Title from "./Title.vue";
import Loader from "./Loader.vue";
import klixxDB from "../assets/klixx.sqlite?url";
import sqlWasm from "sql.js/dist/sql-wasm.wasm?url";
import initSqlJs from "sql.js";

export default {
  name: "home",
  data() {
    return {
      database: null,
      larsColor: "#B782A2",
      florentinColor: "#66748C",
      resultColor: "#D3BD94",
      loaded: false,
      colorBlindMode: false,
    };
  },
  methods: {
    toggleColorBlindness: function () {
      this.colorBlindMode = !this.colorBlindMode;
      if (this.colorBlindMode) {
        this.larsColor = "#AF2E96";
        this.florentinColor = "#AFCAF9";
        this.resultColor = "#DCDC26";
      } else {
        this.larsColor = "#B782A2";
        this.florentinColor = "#66748C";
        this.resultColor = "#D3BD94";
      }
    },
  },
  components: {
    BarChart,
    HorizontalBarChart,
    DoughnutChart,
    VultureKing,
    Table,
    Title,
    ColorCorrectionButton,
    Loader,
  },
  mounted() {
    initSqlJs({
      locateFile: () => sqlWasm,
    }).then((SQL) => {
      // Load the db
      fetch(klixxDB).then((res) => {
        res.arrayBuffer().then((buf) => {
          const buffer = new Uint8Array(buf);
          this.database = new SQL.Database(buffer);
          this.loaded = true;
        });
      });
    });
  },
};
</script>

<style scoped>
.row {
  margin-top: 1.5rem;
}
h2 > a {
  text-decoration: none;
  color: inherit;
}
</style>
