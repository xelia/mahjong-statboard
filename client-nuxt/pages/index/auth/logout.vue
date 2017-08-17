<template>
  <p>Signing off...</p>
</template>

<script>
import { unsetToken } from '~/utils/auth'
export default {
  middleware: ['authenticated'],
  mounted () {
    unsetToken()
    this.$router.push('/')
  }
}
</script>
