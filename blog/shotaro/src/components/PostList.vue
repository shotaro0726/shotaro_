<template>
  <div :key="getKey" class="container">
    <p id="lead">{{ postCount }}件中{{ postRangeFirst }}~{{ postRangeLast }}件の一覧を表示したお</p>
    <section>
      <router-link
        :to="{ name: 'detail', params: {id: post.id}}"
        v-for="post of postList"
        :key="post.id"
        class="post"
      >
        <article>
          <figure>
            <img :src="post.thumbnail" :alt="post.title" class="thumbnail" />
          </figure>
          <p class="post-category" :style="{'color': post.category.color}">{{ post.category.name }}</p>
          <h2 class="post-title">{{ post.title }}</h2>
          <p class="post-lead">{{ post.lead_text }}</p>
        </article>
      </router-link>
    </section>
    <hr class="divider" />
    <nav id="page">
      <route-link v-if="hasPrevious" :to="getPostPreviousURL" id="back">
        <img src="@/assets/back.png" />
      </route-link>
      <span>Page {{ postCurrentPageNumber }}</span>
      <router-link v-if="hasNext" :to="getPostNextURL" id="next">
        <img src="@/assets/next.png" />
      </router-link>
    </nav>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { UPDATE_POSTS } from "../store/mutation-types";

export default {
  name: "post-list",
  watch: {
    $route() {
      this.getPosts();
    }
  },
  created() {
    this.getPosts();
  },
  mounted() {
    document.title = `Shotaro Ooki`;
    document
      .querySelector('meta[name="description"]')
      .setAttribute("content", "アウトプットと技術");
  },
  computed: {
    ...mapGetters([
      "postList",
      "postCount",
      "postRangeFirst",
      "postRangeLast",
      "postCurrentPageNumber",
      "hasPrevious",
      "hasNext",
      "getPreviousURL",
      "getNextURL"
    ]),
    getKey() {
      return `${this.postCurrentPageNumber}${this.$route.query.keyword}${this.$route.query.category}`;
    },
    getPostPreviousURL() {
      const url = new URL(this.getPreviousURL);
      const keyword = url.searchParams.get("keyword") || "";
      const category = url.searchParams.get("category") || "";
      const page = url.searchParams.get("page") || 1;
      return this.$router.resolve({
        name: "posts",
        query: { keyword, category, page }
      }).route.fullPath;
    },
    getPostNextURL() {
      const url = new URL(this.getNextURL);
      const keyword = url.searchParams.get("keyword") || "";
      const category = url.searchParams.get("category") || "";
      const page = url.searchParams.get("page");
      return this.$router.resolve({
        name: "posts",
        query: { keyword, category, page }
      }).route.fullPath;
    }
  },
  methods: {
    ...mapActions([UPDATE_POSTS]),
    getPosts() {
      let postURL = this.$httpPosts;
      const params = this.$route.query;
      const queryString = Object.keys(params)
        .map(key => key + "=" + params[key])
        .join("&");
      if (queryString) {
        postURL += "?" + queryString;
      }
      this.$http(postURL)
        .then(response => {
          return response.json();
        })
        .then(data => {
          this[UPDATE_POSTS](data);
        });
    }
  }
};
</script>

<style scoped>
#lead {
  color: #999999;
}

section {
  margin-top: 80px;
}

.thumbnail {
  width: 100%;
  height: auto;
  vertical-align: bottom;
}

.post {
  text-decoration: none;
  color: green;
  margin-bottom: 80px;
  display: block;
}

.post-category {
  margin-top: 16px;
  font-size: 12px;
}

.post-title {
  font-weight: bold;
  font-size: 14px;
  width: 100%;
}

.post-lead {
  margin-top: 10px;
  width: 100%;
}

.divider {
  margin-top: 50px;
  margin-bottom: 25px;
  width: 100%;
  height: 0;
  border: solid 1px #ccc;
}

#page {
  color: #999;
}

#back {
  width: 44px;
  margin-right: 16px;
  display: inline-block;
}

#next {
  margin-left: 44px;
  width: 44px;
  display: inline-block;
}

@media (min-width: 768px) {
  section {
    display: grid;
    grid-template-columns: 340px 340px;
    column-gap: 20px;
    row-gap: 100px;
  }

  .thumbnail {
    width: 340px;
    height: 215px;
    object-fit: cover;
  }

  .post {
    margin-bottom: 0;
  }

  .post-title {
    width: 280px;
  }

  .post-lead {
    width: 280px;
  }

  .divider {
    width: 650px;
  }
}

@media (min-width: 1024px) {
  section {
    grid-template-columns: 480px 480px;
  }

  .thumbnail {
    width: 480px;
    height: 300px;
  }

  .post-title {
    width: 440px;
  }

  .post-lead {
    width: 440px;
  }
}
</style>