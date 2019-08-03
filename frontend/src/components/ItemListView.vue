<template>
  <div>
    <section class="hero is-info is-bold">
      <div class="hero-body">
        <div class="container">
          <h1 class="title has-text-centered">{{ typeDisplay }}</h1>
        </div>
      </div>
      <div class="hero-foot">
        <div class="container">
          <nav class="tabs is-boxed">
            <ul>
              <li v-for="item in menu" :key="item.name" @mouseover="mouseOver(item, $event)"
                  :class="{'is-active': item.isActive }">
                <a>{{ item.name }}</a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </section>
    <nav class="navbar has-shadow">
      <div class="container">
        <div class="navbar-tabs">
          <router-link class="navbar-item is-tab" v-for="item in subMenu" :key="item.displayValue" :to="item.href">
            {{ item.displayValue }}
          </router-link>
        </div>
      </div>
    </nav>
    <section class="section" v-if="type">
      <div class="container items">
        <div class="columns">
          <div class="column is-one-fifth">
            <div class="field">
              <p class="control" @keyup.enter="search">
                <my-input :value="searchQuery" @input="setSearchQuery"  placeholder="Nazwa albo lvl"/>
              </p>
            </div>
          </div>
          <div class="column is-three-fifths">
            <div class="select">
              <select v-model="selectedBonus">
                <option value="" selected>-- Bonus --</option>
                <option v-for="(val, key) in ITEM_BONUS" :value="key">{{ val.translation }}</option>
              </select>
            </div>
            <div class="select">
              <select v-model="selectedProf">
                <option value="" selected>-- Profesja -</option>
                <option v-for="obj in profsInOrder" :value="obj.value">{{ obj.name }}</option>
              </select>
            </div>
            <div class="select">
              <select v-model="selectedRarity">
                <option value="" selected>-- Rzadkość -</option>
                <option v-for="(val, key) in ITEM_RARITY" :value="key">{{ val }}</option>
              </select>
            </div>
          </div>
          <div class="column is-one-fifth has-text-right">
            <button class="button is-info" @click="search" :disabled="isSearchDisabled">Szukaj</button>
          </div>
        </div>
        <template v-if="!isLoading">
          <msg v-if="itemCount === 0">Nie znaleziono przedmiotów</msg>
          <h1 class="title mb1 has-text-centered" v-else-if="itemCount">{{ itemCount }} przedmiotów</h1>
        </template>
        <section class="hero mt2" v-for="(val, key, index) in items" :class="[index % 2 !== 0 ? 'is-light' : 'is-light2']">
          <div class="hero-head" style="padding-top: 1rem">
            <h1 class="title has-text-centered">{{ key }}</h1>
          </div>
          <div class="hero-body">
            <item v-for="item in val" :key="item.pk" :data="item" :action="RIGHT_CLICK_MAPPER.add"/>
          </div>
        </section>
        <div class="mt1 has-text-centered">
          <button v-if="next && !isLoading" class="button is-info is-medium" @click="loadMore">Pokaż więcej</button>
          <my-spinner v-if="isLoading" size="100"/>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
  import { mapMutations } from 'vuex'
  import { MAP_TYPE_NAME_TO_ID, MENU_LINKS } from '../utils/navbar'
  import Item from './item/Item'
  import { RIGHT_CLICK_MAPPER } from '../utils/constants'
  import { fetchItems } from '../api/items'
  import {getItemLvlGroups, getProfsInOrder} from '../utils/helpers'
  import groupBy from 'lodash/groupBy'
  import { ITEM_BONUS, ITEM_RARITY } from '../utils/items'

  export default {
    name: 'items',
    components: {Item},
    props: ['type'],
    data () {
      return {
        menu: MENU_LINKS,
        subMenu: [],
        items: [],
        RIGHT_CLICK_MAPPER: RIGHT_CLICK_MAPPER,
        isLoading: true,
        next: null,
        searchQuery: '',
        lvlGroups: getItemLvlGroups(),
        defaultGroupName: '0',
        ITEM_BONUS: ITEM_BONUS,
        ITEM_RARITY: ITEM_RARITY,
        profsInOrder: getProfsInOrder(),
        selectedBonus: '',
        selectedProf: '',
        selectedRarity: '',
        itemCount: false,
        searched: false
      }
    },
    mounted () {
      this.getItems()
      for (let i = 0; i < MENU_LINKS.length; i += 1) {
        const subLinks = MENU_LINKS[i].sublinks
        for (let j = 0; j < subLinks.length; j += 1) {
          if (subLinks[j].href.params.type === this.type) {
            MENU_LINKS[i].isActive = true
            this.subMenu = subLinks
            return
          }
        }
      }
    },
    watch: {
      '$route' (to, from) {
        if (!this.type) {
          this.$Progress.finish()
        }
        this._fetchItems()
      }
    },
    computed: {
      isSearchDisabled () {
        return this.fieldsAreEmpty && !this.searched
      },
      typeId () {
        if (this.type) {
          return MAP_TYPE_NAME_TO_ID[this.type]
        }
        return null
      },
      fieldsAreEmpty () {
        return !this.selectedBonus && !this.selectedProf && !this.selectedRarity && !this.searchQuery
      },
      typeDisplay () {
        for (let i = 0; i < MENU_LINKS.length; i += 1) {
          const subLinks = MENU_LINKS[i].sublinks
          for (let j = 0; j < subLinks.length; j += 1) {
            if (subLinks[j].href.params.type === this.type) {
              const text = subLinks[j].displayValue
              this.$setPageTitle(text)
              return text
            }
          }
        }
        this.$setPageTitle('Wybierz typ przedmiotów')
        return 'Wybierz typ przedmiotów'
      }
    },
    methods: {
      ...mapMutations(['setAPIError']),
      mouseOver (item, event) {
        this.menu.map((el) => {
          el.isActive = false
        })
        item.isActive = true
        this.subMenu = item.sublinks
      },
      getItems () {
        if (this.typeId) {
          this._fetchItems()
        } else {
          this.$Progress.finish()
        }
      },
      search () {
        if (!this.isSearchDisabled) {
          this.$Progress.start()
          this._fetchItems()
          this.searched = !this.fieldsAreEmpty
        }
      },
      setSearchQuery (value) {
        this.searchQuery = value
      },
      _fetchItems () {
        if (!this.typeId) {
          return
        }
        this.items = []
        this.isLoading = true
        const qs = `?t=${this.typeId}&per_page=100&n=${this.searchQuery}&p=${this.selectedProf}&b=${this.selectedBonus}&r=${this.selectedRarity}`
        fetchItems(qs, response => {
          this.items = groupBy(response.data.results, item => {
            const group = this.lvlGroups.find(grp => item.lvl >= grp.min)
            return group ? group.name : this.defaultGroupName
          })
          this.itemCount = response.data.count
          this.isLoading = false
          this.$Progress.finish()
          this.next = response.data.next
        }, () => {
          this.setAPIError()
        })
      },
      loadMore () {
        if (!this.next || this.isLoading) {
          return
        }
        this.isLoading = true
        fetchItems(this.next, response => {
          response.data.results.forEach(item => {
            const group = this.lvlGroups.find(grp => item.lvl >= grp.min)
            const groupName = group ? group.name : this.defaultGroupName
            if (groupName in this.items) {
              this.items[groupName].push(item)
            } else {
              this.items[groupName] = [item]
            }
          })
          this.isLoading = false
          this.next = response.data.next
        }, () => {
          this.setAPIError()
        }, true)
      }
    }
  }
</script>

<style scoped>
  .container.items {
    padding: 0
  }
  @media screen and (min-width: 1024px) {
    .container.items {
      padding: 0 2rem
    }
  }

</style>