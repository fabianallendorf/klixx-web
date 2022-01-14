<template>
  <div>
    <div class="row">
      <div class="six columns">
        <button @click="prev">&#129040; Zurück</button>
      </div>
      <div class="six columns">
        <button @click="next">Weiter &#129042;</button>
      </div>
    </div>
    <div v-show="currentItem == 0">
      <div class="row">
        <h4 style="padding-top: 2rem">Objektive Definition</h4>
        <p>
          Die Frage nach dem Geierkönig ist nicht ganz einfach zu beantworten,
          wenn man nur die gesammelten Daten betrachtet. Die Absicht der Spieler
          ist nicht immer klar, obwohl ich davon ausgehe, dass beide darauf
          bedacht sind möglichst nicht zu geiern. Deshalb habe ich mich dazu
          entschieden meine eigene objektive Definition für das
          <em>geiern</em> zu finden.
        </p>
        <p>
          <i>
            Es wurde <b>gegeiert</b>, sobald ein Spieler seinen Tipp zuletzt
            abgibt und die Zahl näher am Tipp des ersten Spielers ist, als an
            der eigentlichen Viewzahl des Videos.
          </i>
        </p>
        <p>
          Beispiel:<br />
          Florentin beginnt<br />
          Florentin tippt 15<br />
          Lars tippt 25<br />
          Video hat 500 Views<br />
          <b>Lars hat hier gegeiert</b>
        </p>
        <p>
          Wenn dieser Fall eintritt, gehe ich davon aus, dass sich der zweite
          Spieler am ersten Spieler orientiert hat um mit seinem Tipp einen
          Vorteil zu erzielen. Im Beispiel hat Lars, Florentin mit seinem Tipp
          zwischen 0 und 25 <i>eingesperrt</i>. Somit hat Lars eine höhere a
          priori Gewinnchance.
        </p>
      </div>
      <div class="row">
        <DoughnutChart
          type="VULTURE_DATA_ORIENTED"
          :db="db"
          :backgroundColor="[florentinColor, larsColor]"
        />
      </div>
      <div>
        <p>
          Es ist unglaublich knapp. <strong>Lars</strong> ist nach aktuellen
          Stand und meiner Definition der echte Geierkönig. Jedoch glaube ich,
          dass beide Spieler fair sind und das Spiel respektieren. Ich habe
          leider die Umfrage am Ende nicht getrackt um einen Vergleich zu
          erstellen.
          <a
            href="https://github.com/fabianallendorf/klixx-data#kann-ich-helfen"
            target="_blank"
            >Vielleicht kann mir jemand helfen? :)</a
          >
        </p>
      </div>
    </div>
    <div v-show="currentItem == 1">
      <div class="row">
        <h4 style="padding-top: 2rem">Der "Geier-Korridor"</h4>
        <p>
          Der fleißige
          <a
            href="https://github.com/fabianallendorf/klixx-data/issues/3#issuecomment-851068557"
            >klauskoflattich</a
          >
          hat fantastische Arbeit geleistet um aus den bekannten Daten das
          <em>Geiern</em> mit Hilfe eines <b>Höflichkeitsabstandes</b> zu
          definieren. Genaueres gibt es im verlinkten Github Kommentar
          nachzulesen. Dieser Höflichkeitsabstand lässt sich sehr gut über einen
          Scatterplot der Schätzungen beider Spieler visualiseren.
        </p>
        <p></p>
      </div>
      <div class="row">
        <ScatterChart
          type="VULTURE_CORRIDOR_DEFINITION_SCATTER_PLOT"
          :db="db"
          :show="currentItem == 1"
          :height="600"
          :scales="{
            x: {
              type: 'logarithmic',
              title: { display: true, text: 'Lars Schätzung' },
            },
            y: {
              type: 'logarithmic',
              title: {
                display: true,
                text: 'Florentin Schätzung',
              },
            },
          }"
          :backgroundColor="[larsColor, florentinColor]"
        />
      </div>
      <div>
        <p>
          Wenn die Achsen logarithmisch skaliert sind, bildet sich ein
          diagonaler Korridor im 45° Winkel mit merklich weniger Punkten. Würden
          beide Spieler gleich schätzen, läge ein Punkt exakt auf dieser
          Diagonalen. Das bedeutet, je näher die Schätzungen beider Spieler
          sind, desto näher liegen die Punkte an dieser gedachten Geraden. Die
          Punkte sind eingefärbt, je nachdem wer welcher Spieler als erster
          geschätzt hat.<br />
          <span class="point" :style="{ color: larsColor }">&#9679;</span>
          bedeutet Lars hat angefangen.
          <br />
          <span class="point" :style="{ color: florentinColor }">&#9679;</span>
          bedeutet Florentin hat zuerst getippt. <br />
        </p>
        <p>
          klauskoflattich schlägt zwei Geraden vor um diesen Korridor zu
          erfassen. Die Geraden würden die X-Achse bei jeweils 0,2 (Untergrenze)
          und -0,2 (Obergrenze) schneiden. Daraus ergibt sich folgende
          Definition:
        </p>
        <p>
          <em
            >Es wurde <b>gegeiert</b>, sobald ein Spieler als zweiter Schätzer
            <b>nicht mehr als das 1,6-fache</b> oder
            <b>nicht weniger als das 0,625-fache</b> schätzt.</em
          >
        </p>
        <p>
          Beispiel:<br />
          Lars beginnt<br />
          Lars tippt 100<br />
          Florentin tippt weniger als 160 <i>oder</i> mehr als 63<br />
          <b>Florentin hat hier gegeiert</b>
        </p>
      </div>
      <div class="row">
        <DoughnutChart
          type="VULTURE_CORRIDOR_DEFINITION_VULTURE"
          :db="db"
          :show="currentItem == 1"
          :backgroundColor="[larsColor, florentinColor]"
        />
      </div>
      <div class="row">
        <p>
          <b>Florentin</b> ist nach dieser Definition ganz klarer Geierkönig mit
          49 Geier-Straftaten. Lars ist dagegen mit nur 22 solcher
          Unsportlichkeiten vom Publikum zu unrecht gepeinigt.
        </p>
      </div>
    </div>
  </div>
</template>
<script>
import DoughnutChart from "./DoughnutChart.vue";
import ScatterChart from "./ScatterChart.vue";

export default {
  name: "VultureKing",
  props: ["larsColor", "florentinColor", "db"],
  components: {
    DoughnutChart,
    ScatterChart,
  },
  data() {
    return {
      items: [0, 1],
      currentItem: 0,
    };
  },
  methods: {
    next: function () {
      if (this.items.includes(this.currentItem + 1)) {
        this.currentItem++;
      }
    },
    prev: function () {
      if (this.currentItem > 0) {
        this.currentItem--;
      }
    },
  },
};
</script>
<style scoped>
.point {
  font-size: 20px;
}
</style>
