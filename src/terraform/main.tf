resource "terraform_data" "test" {
  for_each = { for inst in var.servers : "${inst.name}-${inst.port}" => inst}
  connection {
    type     = "ssh"
    user     = each.value.user
    password = each.value.password
    host     = each.value.name
    port     = each.value.port
  }
  triggers_replace = [
    timestamp()
  ]

  provisioner "remote-exec" {
    inline = [
      "hostname -f",  #GET HOSTNAME OF REMOTE SYSTEM
      "apt list openssh-server -a", #LIST IF OPENSSH-SERVER IS INSTALLED
      "apt list openssh-client -a" #LIST IF OPENSSH-CLIENT IS INSTALLED
    ]
  }
  
  provisioner "local-exec" {
    command = "nc -vz localhost ${each.value.port}" #CHECK IF PORT IS RESPONDING
  }

  provisioner "file" {
    content      = templatefile("${path.module}/sshd_config.tftpl", { 
        UsePAM = "yes", 
        X11Forwarding = "yes", 
        PrintMotd = "no",
        KbdInteractiveAuthentication = "no",
        LoginGraceTime = "2m",
        MaxAuthTries = 4
    })
    destination = "/tmp/sshd_config"
  }

  provisioner "remote-exec" {
    inline = [
      "echo ${each.value.password} | sudo -S cp /tmp/sshd_config /etc/sshd_config -f",
      "echo ${each.value.password} | sudo -S systemctl restart ssh"
    ]
  }
}