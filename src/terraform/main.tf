resource "terraform_data" "test" {
  for_each = { for inst in var.servers : "${inst.name}-${inst.port}" => inst}
  connection {
    type     = "ssh"
    user     = each.value.user
    password = each.value.password
    host     = each.value.name
    port     = each.value.port
    timeout  = "5s"
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
    on_failure = fail
  }
  
  provisioner "local-exec" {
    command = "nc -vz -w 3 localhost ${each.value.port}" #CHECK IF PORT IS RESPONDING
    on_failure = fail
  }

  provisioner "file" {
    content      = templatefile("${path.module}/sshd_config.tftpl", { 
        UsePAM = "yes", 
        X11Forwarding = "yes", 
        PrintMotd = "no",
        KbdInteractiveAuthentication = "no",
        LoginGraceTime = "2m",
        MaxAuthTries = 4,
        ListenAddress = "0.0.0.0",
        LogLevel = "INFO",
        MaxSessions = 10,
        IgnoreUserKnownHosts = "no",
        PasswordAuthentication = "yes"
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