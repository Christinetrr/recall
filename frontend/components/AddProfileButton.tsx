"use client";

import { useMemo, useState } from "react";

type FormState = {
  name: string;
  relation: string;
  imageName: string;
};

const initialFormState: FormState = {
  name: "",
  relation: "",
  imageName: "",
};

export default function AddProfileButton() {
  const [isOpen, setIsOpen] = useState(false);
  const [formState, setFormState] = useState<FormState>(initialFormState);

  const disabled = useMemo(() => {
    return !formState.name || !formState.relation || !formState.imageName;
  }, [formState]);

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        className="rounded-full bg-zinc-900 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-zinc-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-zinc-900"
      >
        Add Profile
      </button>

      {isOpen ? (
        <>
          <button
            type="button"
            aria-label="Close add profile form"
            className="fixed inset-0 z-40 cursor-default bg-black/10"
            onClick={() => {
              setIsOpen(false);
              setFormState(initialFormState);
            }}
          />
          <div className="absolute right-0 z-50 mt-3 w-80 rounded-2xl border border-zinc-200 bg-white p-5 shadow-2xl">
            <div className="flex items-start justify-between">
              <h2 className="text-base font-semibold text-zinc-900">
                Add Profile
              </h2>
              <button
                type="button"
                onClick={() => {
                  setIsOpen(false);
                  setFormState(initialFormState);
                }}
                className="text-sm text-zinc-400 transition hover:text-zinc-600"
              >
                Close
              </button>
            </div>
            <p className="mt-1 text-sm text-zinc-500">
              Provide the person&apos;s details and upload a profile photo.
            </p>

            <form
              className="mt-4 space-y-4"
              onSubmit={(event) => {
                event.preventDefault();
                setIsOpen(false);
                setFormState(initialFormState);
              }}
            >
              <label className="block text-sm font-medium text-zinc-700">
                Name
                <input
                  type="text"
                  name="name"
                  placeholder="e.g. Andrea Martinez"
                  value={formState.name}
                  onChange={(event) =>
                    setFormState((prev) => ({
                      ...prev,
                      name: event.target.value,
                    }))
                  }
                  className="mt-1 w-full rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900 shadow-sm focus:border-zinc-900 focus:outline-none focus:ring-2 focus:ring-zinc-900/10"
                  required
                />
              </label>

              <label className="block text-sm font-medium text-zinc-700">
                Relation
                <input
                  type="text"
                  name="relation"
                  placeholder="e.g. Friend"
                  value={formState.relation}
                  onChange={(event) =>
                    setFormState((prev) => ({
                      ...prev,
                      relation: event.target.value,
                    }))
                  }
                  className="mt-1 w-full rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900 shadow-sm focus:border-zinc-900 focus:outline-none focus:ring-2 focus:ring-zinc-900/10"
                  required
                />
              </label>

              <label className="block text-sm font-medium text-zinc-700">
                Image
                <input
                  type="file"
                  name="image"
                  accept="image/*"
                  onChange={(event) =>
                    setFormState((prev) => ({
                      ...prev,
                      imageName: event.target.files?.[0]?.name ?? "",
                    }))
                  }
                  className="mt-1 w-full rounded-lg border border-dashed border-zinc-300 bg-zinc-50 px-3 py-6 text-sm text-zinc-500 shadow-sm file:mr-4 file:cursor-pointer file:rounded-md file:border-0 file:bg-zinc-900 file:px-3 file:py-2 file:text-sm file:font-medium file:text-white hover:border-zinc-400 focus:border-zinc-900 focus:outline-none focus:ring-2 focus:ring-zinc-900/10"
                  required
                />
                {formState.imageName ? (
                  <span className="mt-1 block text-xs text-zinc-400">
                    Selected: {formState.imageName}
                  </span>
                ) : null}
              </label>

              <button
                type="submit"
                disabled={disabled}
                className="w-full rounded-full bg-zinc-900 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-zinc-700 disabled:cursor-not-allowed disabled:bg-zinc-300"
              >
                Submit
              </button>
            </form>
          </div>
        </>
      ) : null}
    </div>
  );
}

