<template>
  <div class="columns">
    <div class="column" v-for="eqItems in eqHistory">
      <eq :source="eqItems" :readOnly="true" darkBorder></eq>
      <span>kopiuj link</span>
      <router-link :to="getEqLink(eqItems)">Przejdź do zestawu</router-link>
      <button class="button is-dark" @click="copyEq(eqItems)">Zapisz jako moje</button>
      <router-link :to="getCompareEqLink(eqItems)">Porównaj z moim</router-link>
    </div>
  </div>
  <!--<section>-->
  <!--<b-collapse class="card" :open.sync="isOpen">-->
  <!--<div slot="trigger" class="card-header">-->
  <!--<p class="card-header-title">-->
  <!--Ostatnio przeglądane zestawy {{ eqHistory.length }}-->
  <!--</p>-->
  <!--&lt;!&ndash;<a class="card-header-icon">&ndash;&gt;-->
  <!--&lt;!&ndash;<b-icon :icon="isOpen ? 'menu-down' : 'menu-up'"></b-icon>&ndash;&gt;-->
  <!--&lt;!&ndash;</a>&ndash;&gt;-->
  <!--</div>-->
  <!--<div class="card-content">-->
  <!--<div class="content">-->
  <!--Możesz zobaczyć 5 ostatnich odwiedzanych zestawów.-->
  <!--<button class="button is-dark" @click="showNext">Następny</button>-->
  <!--<eq :source="currentEqItems" :readOnly="true"></eq>-->
  <!--</div>-->
  <!--</div>-->
  <!--<footer class="card-footer">-->
  <!--<button class="card-footer-item">kopiuj link</button>-->
  <!--<router-link class="card-footer-item" :to="getEqLink(currentEqItems)">Przejdź do zestawu</router-link>-->
  <!--<button class="card-footer-item" @click="saveAsMine(currentEqItems)">Zapisz jako moje</button>-->
  <!--</footer>-->
  <!--</b-collapse>-->
  <!--</section>-->

  <!--<b-tabs v-model="current">-->
  <!--<b-tab-item label="Pictures">-->
  <!--<eq :source="currentEqItems" :readOnly="true"></eq>-->
  <!--</b-tab-item>-->

  <!--<b-tab-item label="Music">-->
  <!--Lorem <br>-->
  <!--ipsum <br>-->
  <!--dolor <br>-->
  <!--sit <br>-->
  <!--amet.-->
  <!--</b-tab-item>-->
  <!--</b-tabs>-->
  <!-- <section class="section">
    <eq-summary :source="eqSetStats"></eq-summary>
  </section> -->
</template>

<script>
  import { getCompareEqLink, getEqRoute } from '../../utils/helpers'
  import { mapGetters } from 'vuex'
  import { copyEq } from '../mixins/copyEq'
  import Eq from '../eq/Eq'

  export default {
    name: 'eq-history',
    components: {Eq},
    mixins: [copyEq],
    data () {
      return {
        isOpen: true,
        current: 0
      }
    },
    computed: {
      ...mapGetters(['eqHistory']),
      currentEqItems: function () {
        return this.eqHistory[this.current]
      }
    },
    methods: {
      getEqLink: eqItems => getEqRoute(eqItems),
      getCompareEqLink: getCompareEqLink
    }
  }
</script>

<style scoped>

</style>
