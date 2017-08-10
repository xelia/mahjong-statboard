export default function({app, redirect, route}) {
  app.$axios.get(`/auth/user/?format=json`).then(
    (data) => {
      if(!data.is_authenticated){
        return redirect(`/admin/login/?next=${route.path}`)
      }
    }
  )

}
