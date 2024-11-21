variable "servers" {
  description = "List of remote servers"
  type = list(object({
    name        = string,
    port        = string,
    user        = string,
    password    = string,
  }))
  default = [
    {
      name = "localhost",
      port = "8022",
      user = "ch"
      password = "ch"
    },
    {
      name = "localhost",
      port = "8122",
      user = "ch"
      password = "ch"
    }
  ]
}