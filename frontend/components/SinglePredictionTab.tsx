"use client";

import { ImagePlus, Loader2, UploadCloud } from "lucide-react";

type SinglePredictionTabProps = {
  singlePreview: string | null;
  singleFile: File | null;
  singleFruit: string | null;
  singleConfidence: number | null;
  singleLoading: boolean;
  inputRef: React.RefObject<HTMLInputElement | null>;
  inputKey: number;
  onUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onPredict: () => void;
  onReset: () => void;
};

export default function SinglePredictionTab({
  singlePreview,
  singleFile,
  singleFruit,
  singleConfidence,
  singleLoading,
  inputRef,
  inputKey,
  onUpload,
  onPredict,
  onReset,
}: SinglePredictionTabProps) {
  return (
    <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
      <div className="rounded-[24px] border border-gray-200 bg-[#fafaf8] p-5 md:p-6">
        <div className="mb-5">
          <h2 className="text-xl font-medium text-[#111]">
            Single image prediction
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Upload one fruit image and get a clean prediction with confidence.
          </p>
        </div>

        <label className="group flex min-h-[240px] cursor-pointer flex-col items-center justify-center rounded-[24px] border-2 border-dashed border-gray-300 bg-white px-6 text-center transition-all duration-300 hover:border-green-500 hover:bg-green-50/40">
          <input
            key={inputKey}
            ref={inputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={onUpload}
          />

          {singlePreview ? (
            <div className="w-full">
              <img
                src={singlePreview}
                alt="Selected fruit"
                className="mx-auto h-56 w-full max-w-md rounded-2xl object-contain"
              />
              <p className="mt-4 text-sm font-medium text-gray-700">
                {singleFile?.name}
              </p>
              <p className="mt-1 text-xs text-gray-500">Tap to replace image</p>
            </div>
          ) : (
            <>
              <div className="mb-4 rounded-full bg-green-100 p-4 text-green-700">
                <UploadCloud size={28} />
              </div>
              <p className="text-base font-medium text-[#111]">
                Click to upload an image
              </p>
              <p className="mt-2 text-sm text-gray-500">
                PNG, JPG, JPEG supported
              </p>
            </>
          )}
        </label>

        <div className="mt-5 flex flex-wrap gap-3">
          <button
            type="button"
            onClick={onPredict}
            disabled={singleLoading}
            className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-green-600 via-emerald-700 to-green-600 px-5 py-3 text-sm font-medium text-white transition-all duration-300 hover:from-green-600 hover:via-emerald-600 hover:to-green-700 hover:shadow-lg active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {singleLoading ? (
              <span className="flex items-center gap-2">
                <Loader2 size={16} className="animate-spin" />
                Predicting...
              </span>
            ) : (
              "Predict Fruit"
            )}
          </button>

          {singleFile && (
            <button
              type="button"
              onClick={onReset}
              className="rounded-full bg-gray-100 px-5 py-3 text-sm font-medium text-gray-700 transition hover:bg-gray-200"
            >
              Reset
            </button>
          )}
        </div>
      </div>

      <div className="rounded-[24px] border border-gray-200 bg-white p-5 md:p-6">
        <h3 className="text-xl font-medium text-[#111]">Prediction result</h3>
        <p className="mt-2 text-sm text-gray-600">
          Your AI result will appear here.
        </p>

        <div className="mt-6 flex min-h-[280px] items-center justify-center rounded-[24px] bg-[#f8faf8] p-6">
          {singleFruit && singleConfidence !== null ? (
            <div className="w-full">
              <div className="mb-4 inline-flex rounded-full bg-green-100 px-4 py-2 text-sm font-medium text-green-700">
                Prediction complete
              </div>

              <h4 className="text-3xl font-semibold text-[#111]">
                {singleFruit}
              </h4>

              <div className="mt-6">
                <div className="mb-2 flex items-center justify-between text-sm text-gray-600">
                  <span>Confidence</span>
                  <span>{singleConfidence}%</span>
                </div>

                <div className="h-3 w-full overflow-hidden rounded-full bg-gray-200">
                  <div
                    className="h-full rounded-full bg-green-600 transition-all duration-500"
                    style={{
                      width: `${Math.min(Number(singleConfidence), 100)}%`,
                    }}
                  />
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-500">
              <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-gray-100">
                <ImagePlus size={24} />
              </div>
              <p className="text-sm">
                Upload an image and run prediction to see the result
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
