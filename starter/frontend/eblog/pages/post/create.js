import Post from "@/components/postForm";
import { useAuthToken } from "@/contexts/context";
import Head from "next/head";
import { useRouter } from "next/router";
import { useRef } from "react";
import useSWRMutation from "swr/mutation";

export default function Create() {
  //auth
  const accessToken = useAuthToken();

  // router
  const router = useRouter();

  // ref
  const formRef = useRef();

  // remote mutate
  const { data: post, trigger: createPost } = useSWRMutation(
    `http://127.0.0.1:5000/post/`,
    async (url, { arg }) => {
      const post = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: arg,
      })
        .then((res) => res.json())
        .then((data) => data);

      if (post.errors) {
        return post;
      }

      // redirect to list
      router.push("/");
    },
  );

  // create post
  const handleCreatePost = async (e) => {
    e.preventDefault();

    const formDate = new FormData(formRef.current);
    createPost(JSON.stringify({
      subject: formDate.get("subject"),
      content: formDate.get("content"),
    }));
  };

  return (
    <>
      <Head>
        <title>Create Next App</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main>
        <Post
          post={post}
          errors={post && post.errors}
          formRef={formRef}
          onClick={handleCreatePost}
        />
      </main>
    </>
  );
}
