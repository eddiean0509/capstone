import Head from "next/head";
import { useRouter } from "next/router";
import { useRef } from "react";
import useSWR from "swr";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useAuthToken } from "@/contexts/context";
import Link from "next/link";
import FormError from "@/components/formError";
import { useAuth0 } from "@auth0/auth0-react";

const fetcher = (...args) => fetch(...args).then((res) => res.json());

export default function Post() {
  // auth
  const { user } = useAuth0();
  const accessToken = useAuthToken();

  // router
  const router = useRouter();

  // refs
  const formRef = useRef();

  // post
  const {
    data: post,
    error,
    mutate,
  } = useSWR(`${process.env.API_URL}/post/${router.query.id}/`, fetcher, {
    keepPreviousData: true,
    revalidateOnFocus: false,
  });

  // delete post
  const handleDeletePost = (e, postId) => {
    e.preventDefault();
    if (!confirm("Are you sure you want to delete?")) {
      return;
    }
    mutate(
      async () => {
        const deleted = await fetch(`${process.env.API_URL}/post/${postId}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
          .then((res) => res.json())
          .then((data) => data);

        if (deleted.errors) {
          return { ...post, ...deleted };
        }

        router.push("/");
        return;
      },
      { revalidate: false },
    );
  };

  // add post voter
  const handleAddPostVoter = (e, postId) => {
    e.preventDefault();

    if (post.voter.filter((voter) => voter.email == (user && user.email)).length) {
      alert("Already voted.");
      return;
    }
    mutate(
      async () => {
        const voters = await fetch(`${process.env.API_URL}/post/${postId}/vote`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
          .then((res) => res.json())
          .then((data) => data);

        // error
        if (voters.errors) {
          return { ...post, ...voters };
        }

        return { ...post, voter: [...voters], errors: undefined };
      },
      { revalidate: false },
    );
  };

  // add reply voter
  const handleAddReplyVoter = (e, postId, replyId) => {
    e.preventDefault();

    const reply = post.reply_set.filter((reply) => reply.id == replyId)[0];
    if (reply.voter.filter((voter) => voter.email == (user && user.email)).length) {
      alert("Already voted.");
      return;
    }
    mutate(
      async () => {
        const voters = await fetch(
          `${process.env.API_URL}/post/${postId}/reply/${replyId}/vote`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          },
        )
          .then((res) => res.json())
          .then((data) => data);

        // error
        if (voters.errors) {
          return { ...post, ...voters };
        }

        const replys = post.reply_set.map((reply) => {
          if (reply.id == replyId) {
            reply.voter = voters;
          }
          return { ...reply };
        });

        return { ...post, reply_set: [...replys], errors: undefined };
      },
      { revalidate: false },
    );
  };

  // create reply
  const handleCreateReply = (e, postId) => {
    e.preventDefault();

    // remote mutate -> local mutate
    mutate(
      async () => {
        const reply = await fetch(`${process.env.API_URL}/post/${postId}/reply`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
          body: (() => {
            const formDate = new FormData(formRef.current);
            return JSON.stringify({ content: formDate.get("content") });
          })(),
        })
          .then((res) => res.json())
          .then((data) => data);

        // error
        if (reply.errors) {
          return { ...post, ...reply };
        }

        // form textarea
        formRef.current["content"].value = "";

        return {
          ...post,
          reply_set: [...post.reply_set, reply],
          errors: undefined,
        };
      },
      { revalidate: false },
    );
  };

  // delete reply
  const handleDeleteReply = (e, postId, replyId) => {
    e.preventDefault();
    if (!confirm("Are you sure you want to delete?")) {
      return;
    }
    mutate(
      async () => {
        const deleted = await fetch(
          `${process.env.API_URL}/post/${postId}/reply/${replyId}`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          },
        )
          .then((res) => res.json())
          .then((data) => data);

        if (deleted.errors) {
          return { ...post, ...deleted };
        }

        const replys = post.reply_set.filter((reply) => replyId != reply.id);
        return { ...post, reply_set: [...replys], errors: undefined };
      },
      { revalidate: false },
    );
  };

  if (error) return <div>Failed to load</div>;
  if (!post) return <div></div>;

  return (
    <>
      <Head>
        <title>{post.subject}</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main>
        <div className="container my-3">
          <h2 className="border-bottom py-2">{post.subject}</h2>
          <div className="card my-3">
            <div className="card-body">
              <div className="card-text">
                <ReactMarkdown children={post.content} remarkPlugins={[remarkGfm]} />
              </div>
              <div className="d-flex justify-content-end">
                {post.modify_date && (
                  <div className="badge bg-light text-dark p-2 text-start mx-3">
                    <div className="mb-2">modified at</div>
                    <div>{new Date(post.modify_date).toLocaleString("en")}</div>
                  </div>
                )}
                <div className="badge bg-light text-dark p-2 text-start">
                  <div className="mb-2">{post.user.email}</div>
                  <div>{new Date(post.create_date).toLocaleString("en")}</div>
                </div>
              </div>
              <div className="my-3">
                <a
                  href="#"
                  className="recommend btn btn-sm btn-outline-secondary me-1"
                  onClick={(e) => handleAddPostVoter(e, post.id)}
                >
                  {" "}
                  VOTE
                  <span className="badge rounded-pill bg-success ms-2">
                    {post.voter.length}
                  </span>
                </a>
                {user && user.email == post.user.email && (
                  <>
                    <Link
                      href={`/post/modify?id=${post.id}`}
                      className="btn btn-sm btn-outline-secondary me-1"
                    >
                      Modify
                    </Link>
                    <a
                      href="#"
                      className="delete btn btn-sm btn-outline-secondary"
                      onClick={(e) => handleDeletePost(e, post.id)}
                    >
                      Delete
                    </a>
                  </>
                )}
              </div>
            </div>
          </div>
          {post.reply_set.length > 0 ? (
            <h5 className="border-bottom my-3 py-2">
              Check the Reply! count: {post.reply_set.length}
            </h5>
          ) : (
            <h5 className="border-bottom my-3 py-2">The reply does not exist.</h5>
          )}
          {post.reply_set.map((reply) => (
            <div key={reply.id}>
              <a id="reply_{reply.id}"></a>
              <div className="card my-3">
                <div className="card-body">
                  <ReactMarkdown children={reply.content} remarkPlugins={[remarkGfm]} />
                  <div className="d-flex justify-content-end">
                    {reply.modify_date && (
                      <div className="badge bg-light text-dark p-2 text-start mx-3">
                        <div className="mb-2">modified at</div>
                        <div>{new Date(reply.modify_date).toLocaleString("en")}</div>
                      </div>
                    )}
                    <div className="badge bg-light text-dark p-2 text-start">
                      <div className="mb-2">{reply.user.email}</div>
                      <div>{new Date(reply.create_date).toLocaleString("en")}</div>
                    </div>
                  </div>
                  <div className="my-3">
                    <a
                      href="#"
                      className="recommend btn btn-sm btn-outline-secondary me-1"
                      onClick={(e) => handleAddReplyVoter(e, post.id, reply.id)}
                    >
                      {" "}
                      VOTE
                      <span className="badge rounded-pill bg-success ms-2">
                        {reply.voter.length}
                      </span>
                    </a>
                    {user && user.email == reply.user.email && (
                      <>
                        <Link
                          href={`/reply/modify?id=${reply.id}&post_id=${post.id}`}
                          className="btn btn-sm btn-outline-secondary me-1"
                        >
                          Modify
                        </Link>
                        <a
                          href="#"
                          className="delete btn btn-sm btn-outline-secondary "
                          onClick={(e) => handleDeleteReply(e, post.id, reply.id)}
                        >
                          Delete
                        </a>
                      </>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
          <form ref={formRef}>
            {post.errors && <FormError errors={post.errors} />}
            {user && (
              <>
                <div className="mb-3">
                  <textarea
                    disabled={user.email ? false : "disabled"}
                    name="content"
                    id="content"
                    className="form-control"
                    rows="10"
                  ></textarea>
                </div>
                <input
                  type="button"
                  value="Save the Reply"
                  className="btn btn-primary"
                  onClick={(e) => handleCreateReply(e, post.id)}
                />
              </>
            )}
          </form>
        </div>
      </main>
    </>
  );
}
