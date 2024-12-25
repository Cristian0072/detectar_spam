import { redirect } from "next/navigation";
//redireccionar a la pagina de menu
export default function Home() {
  redirect("/menu");
}
